# Meetup - Real-time streaming dashboard

## Screenshots

### Solution Overview - Pipeline runs simultaneously in real-time

![Solution](images/solution_overview.png?raw=true)

- Created a real-time streaming RSVP dashboard which updates every 5 seconds.
- Used the Meetup API. Meetup is an online service where in-person event groups are created and users can confirm their participation in the events.
- Apache Kafka used as a producer to publish the messages to the Spark Stream.
- Spark Streaming is used as a consumer to receive the messages every 5 seconds as a batch.
- Preprocessing done using Spark and map-reduce techniques with the output being stored in Cassandra.
- Single-page interactive visualization dashboard built using ‘Dash by Plotly‘ updated in real-time with the stream every 5 seconds.

### Dashboard
![Dashboard](images/dashboard_overview.png?raw=true)

### Components within Dashboard

#### Statistics Header
- Top header displays and updates the overall metrics of RSVP’s and the last time the dashboard was updated.

![Statistics Header](images/statistics_header.png?raw=true)

#### Click-based Interactive Updates
- Bar graph interacts with the world map based on the area selected on the world map.
  - E.g. we clicked on USA and the bar graph filtered based on that to show the top events trending only in USA.
- Group names are shown on the bars when you hover over them.

![Interactive Updates](images/interactive_updates.png?raw=true)

### Cassandra Tables Excerpts

- Pre-aggregated the data in a distributed fashion using Spark before storing it in Cassandra
- The 3 aggregated tables are stored in Cassandra where the total RSVP count was updated by the stream every 5 seconds.

#### Country Event Statistics Table
![Cassandra Event Stats](images/cassandra_event_stats_table.png?raw=true)

#### Country Statistics Table
![Cassandra Country Stats](images/cassandra_country_stats_table.png?raw=true)

#### Response Statistics Table
![Cassandra Response Stats](images/cassandra_response_stats_table.png?raw=true)
