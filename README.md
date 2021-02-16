# Meetup - Real-time streaming dashboard

• Created a real-time streaming RSVP dashboard which updates every 5 seconds.
• Used the Meetup API. Meetup is an online service where in-person event groups are created and users can confirm their participation in the events.
• Apache Kafka used as a producer to publish the messages to the Spark Stream.
• Spark Streaming is used as a consumer to receive the messages every 5 seconds as a batch.
• Preprocessing done using Spark and map-reduce techniques with the output being stored in Cassandra.
• Single-page interactive visualization dashboard built using ‘Dash by Plotly‘ updated in real-time with the stream every 5 seconds.

## Screenshots

### Solution Overview (Technologies)
![Solution](images/solution_overview.png?raw=true)

### Dashboard Overview
![Dashboard](images/dashboard_overview.png?raw=true)
![Statistics Header](images/statistics_header.png?raw=true)
![Interactive Updates](images/interactive_updates.png?raw=true)

### Cassandra Tables Excerpts
![Cassandra Country Stats](images/cassandra_country_stats_table.png?raw=true)
![Cassandra Event Stats](images/cassandra_event_stats_table.png?raw=true)
![Cassandra Response Stats](images/cassandra_response_stats_table.png?raw=true)
