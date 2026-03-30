FROM apache/airflow:3.1.8

USER airflow

RUN pip install --no-cache-dir \
    gspread \
    google-auth \
    oauth2client \
    pandas \
    pyarrow \
    openpyxl \
    numpy \
    python-dotenv \
    sqlalchemy \
    psycopg2-binary \
    duckdb \
    workalendar \
    apache-airflow-providers-postgres
