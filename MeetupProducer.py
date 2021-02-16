import json
import requests
from kafka import KafkaProducer
from time import sleep
from json import dumps


if __name__ == '__main__':
    print("### Meetup RSVPS Producer is running...")
    
    # Set the Kafka Producer
    topic = "meetuptopic"
    kafkaserver_port = "localhost:9092"
    meetup_producer = KafkaProducer(bootstrap_servers=[kafkaserver_port],
                             value_serializer=lambda x: 
                             dumps(x).encode('utf-8'))
    
    # Access open meetup API
    api_link = "https://stream.meetup.com/2/rsvps"
    print("### Connecting to the api endpoint: " + api_link)
    api_request = requests.get(api_link, stream=True)
    print("### Receiving Meetup records from the api endpoint...")
    
    # Start receiving data from API
    i = 1
    for byte_object in api_request.iter_lines():
        output_json = json.loads(byte_object.decode("utf-8"))   
        # Kafka producer sending the data as long as it's not empty
        if len(output_json) > 0:
            meetup_producer.send(topic, value=output_json)
            print(output_json)
            print("-----------------Meetup API output (RSVP " + str(i) + ")-----------------------------------")
            i += 1