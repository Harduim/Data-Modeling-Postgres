# Data Modeling with Postgres | Udacity Project | rubrics

Main goals of this project:  
- To Define fact and dimension tables for a star schema for a particular analytic focus
- Build an ETL pipeline that transfers data local files into these tables in Postgres using Python and SQL.


## Setting up the environment:

### Requirements:
- [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)
- [Anaconda](https://www.anaconda.com/)

### Database
- Navigate to the project folder
- Create the postgress container: `docker-compose up`
- Create the **sparkifydb** database and tables: `python3 create_tables.py`

### Conda
- Navigate to the project folder
- Create the environment: `conda env create -f environment.yml`
- Activate the new environment: `conda activate rubrics`

## ETL
- Run the ETL pipeline: `python3 etl.py`