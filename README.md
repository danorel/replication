### Instructions

1. `docker-compose up`: starts Master-Slave PostgreSQL database replicas, application service using them.
2. `docker-compose stop`: stops all Docker containers.

### Application

Application web service starts using localhost:8080 URL:

1. Goto `/` to check whether application is running or not.
2. Goto `/database/init` to create Titanic table in replicas.
3. Goto `/write/master` to write random record from Titanic csv to master replica.
4. Goto `/write/slave` to write random record from Titanic csv to slave replica.
5. Goto `/read/master` to read total amount of survived people in Titanic tragedy from master replica.
6. Goto `/read/slave` to read total amount of survived people in Titanic tragedy from slave replica.