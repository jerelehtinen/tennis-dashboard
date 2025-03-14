# tennis-dashboard
Dashboard to view tennis stats


# How to start

Basic use case is to run `docker-compose up --build` which will:
- build all images
- Runs dlt project
- Runs dbt project once dlt is completed
- Starts streamlit app once dbt is completed

To build individual image:
- `docker-compose build dlt`
- `docker-compose build dbt`
- `docker-compose build streamlit`


To individual container:
- `docker-compose up dlt`
- `docker-compose up dbt`
- `docker-compose up streamlit`

