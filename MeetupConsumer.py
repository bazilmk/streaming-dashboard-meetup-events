import json
import pycountry
import pyspark_cassandra
import pyspark_cassandra.streaming

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from cassandra.cluster import Cluster
from pyspark_cassandra import CassandraSparkContext


def create_country_code_map():
    with open('country_codes.txt') as json_file:
        data = json.load(json_file)
        return data

def update_total_count(curr_count, count_state):
    if count_state is None:
       count_state = 0
    return sum(curr_count, count_state)


if __name__ == '__main__':
    
    # Connect to Cassandra
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect()
    
    # Initialize keyspace in Cassandra
    session.execute("CREATE KEYSPACE IF NOT EXISTS meetups_space WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
    
    # Initialize table in Cassandra for country and event statistics
    session.execute("CREATE TABLE IF NOT EXISTS meetups_space.country_statistics (event_country text PRIMARY KEY, total_rsvps int);")
    session.execute("CREATE TABLE IF NOT EXISTS meetups_space.response_statistics (response text PRIMARY KEY, total_rsvps int);")
    session.execute("CREATE TABLE IF NOT EXISTS meetups_space.event_statistics (event_name text, group_name text, event_country text, response text, total_rsvps int, PRIMARY KEY ((event_name), response));")
  
    # Configured the spark stream
    conf = SparkConf().set("spark.cassandra.connection.host", "localhost")
    sc = CassandraSparkContext(appName='MeetupDashboard', conf=conf)
    ssc = StreamingContext(sc, 5)
    ssc.checkpoint("/tmp")
    topic = ["meetuptopic"]
    kafkaConf = {"metadata.broker.list": "localhost:9092",
			"zookeeper.connect": "localhost:2181",
			"group.id": "kafka-spark-streaming",
			"zookeeper.connection.timeout.ms": "1000"}
    
    # DStream
    messages = KafkaUtils.createDirectStream(ssc, topic, kafkaConf)
    
    # Pre-process DStream
    lines = messages.map(lambda (key, values): json.loads(values))
    
    # Compute country statistics
    country_code_map = create_country_code_map()
    country_rsvps = lines.map(lambda country: ((country_code_map[country['group']['group_country']]), 1)).reduceByKey(lambda x, y: x + y)

    # Compute response statistics
    response_rsvps = lines.map(lambda values: (values['response'], 1)).reduceByKey(lambda x, y: x + y)
    
    # Compute event statistics
    event_rsvps = lines.map(lambda event: ((event['event']['event_name'], event['group']['group_name'], country_code_map[event['group']['group_country']], event['response']), 1)).reduceByKey(lambda x, y: x + y)
        
    # Update values 
    updated_country_rsvps = country_rsvps.updateStateByKey(update_total_count)
    updated_response_rsvps = response_rsvps.updateStateByKey(update_total_count)
    updated_event_rsvps = event_rsvps.updateStateByKey(update_total_count)
    updated_event_rsvps = updated_event_rsvps.map(lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[1]))

    # Save processed data to Cassandra
    updated_country_rsvps.saveToCassandra("meetups_space", "country_statistics", columns=['event_country', 'total_rsvps'])   
    updated_response_rsvps.saveToCassandra("meetups_space", "response_statistics", columns=['response', 'total_rsvps'])
    updated_event_rsvps.saveToCassandra("meetups_space", "event_statistics", columns=['event_name', 'group_name', 'event_country', 'response', 'total_rsvps'])


    ssc.start()
    ssc.awaitTermination()
