-- Executado automaticamente pelo Postgres na primeira inicialização do container
-- Cria o schema dedicado para o Airflow dentro do banco SETUP

CREATE SCHEMA IF NOT EXISTS airflow;

-- Garante que o usuário postgres tenha permissão total no schema
GRANT ALL PRIVILEGES ON SCHEMA airflow TO postgres;
