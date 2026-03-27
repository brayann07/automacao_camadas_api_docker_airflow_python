import requests as api_get
import psycopg2 as db_py

## BANCO CONEXÃO ##
try:
    conn = db_py.connect(
        host="seu-host",
        database="seu-database",
        user="seu-nome",
        password="sua-senha",
        port="seu-port"
    )
    print("Conectado com sucesso")
except Exception as error:
    print("Erro na conexão:",error)
    quit()

## variaveis iniciais ##    
cursor = conn.cursor()
nome_schema_extracao = "extracao_palavras_aleatorias"
nome_tabela = "palavras_aleatorias"

## api configs ##
url = "https://random-words-api.kushcreates.com/api?language=pt-br"
res = api_get.get(url)
api_dados = res.json()

if api_dados[0]:
    print("Conseguiu retribuir algum dado")
else:
    print("API SEM DADOS")
    quit()

def cursor_commit_command(command : str):
    cursor.execute(command)
    conn.commit()
def check_if_table_exists(schema_name, table_name):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s
        )
    """, (schema_name, table_name))

    return cursor.fetchone()[0]

def run_sql_file(file_path):
    with open(file_path,'r') as file:
        sql_script = file.read()
    cursor.execute(sql_script)
    conn.commit()
    print(f"RODOU O COMANDO SQL EM:{file_path}") 

##################

#! STAGING INIT VALUES #
init_staging_check_schema = f"""
CREATE SCHEMA IF NOT EXISTS {nome_schema_extracao}
"""
cursor_commit_command(init_staging_check_schema)

check_if_staging_table_exists = check_if_table_exists(nome_schema_extracao,f"staging_{nome_tabela}")
if check_if_staging_table_exists:
    init_staging_truncate_table = f"""
    TRUNCATE TABLE {nome_schema_extracao}.staging_{nome_tabela}
    """
    cursor_commit_command(init_staging_truncate_table)
else:
    init_staging_try_create_table = f"""
    CREATE TABLE {nome_schema_extracao}.staging_{nome_tabela}(
        debug_value text
    )
    """
    cursor_commit_command(init_staging_try_create_table)


#! CAMADA STAGING ADD VALUES ##########################################################################
nomeColunas = []

for item in api_dados:
    for key in item.keys():
        if key not in nomeColunas:
            nomeColunas.append(key)
    print("--------")
    break

print(nomeColunas)

print("GUARDOU VALORES TEMPORARIAMENTE")

# DELETAR VALORES SE EXISTIR(DEBUG)
try_deleting_debug = f"""
    ALTER TABLE {nome_schema_extracao}.staging_{nome_tabela}
    DROP COLUMN IF EXISTS debug_value
"""
cursor_commit_command(try_deleting_debug)
#####################################

for name_coluna in nomeColunas:
    add_columns_inside_staging = f"""
        alter table {nome_schema_extracao}.staging_{nome_tabela}
        add column if not exists {name_coluna} text
    """
    cursor_commit_command(add_columns_inside_staging)

print("CRIOU COLUNAS NA STAGING")

for item in api_dados:
    valores_escapados = [str(item[col]).replace("'", "''") for col in nomeColunas]
    add_values_inside_staging = f"""
        INSERT INTO {nome_schema_extracao}.staging_{nome_tabela}
        VALUES(
            '{str(valores_escapados[0])}',
            '{str(valores_escapados[1])}',
            '{str(valores_escapados[2])}',
            '{str(valores_escapados[3])}'
        )
    """
    cursor_commit_command(add_values_inside_staging)

print("ADICIONOU ESSES VALORES A COLUNAS")

##############################


#################################? CAMADA SILVER #################################################################

check_if_silver_table_exists = check_if_table_exists(nome_schema_extracao,f"silver_{nome_tabela}")

if check_if_silver_table_exists:    
    delete_all_values = f"""
        TRUNCATE TABLE {nome_schema_extracao}.silver_{nome_tabela}
    """
    cursor_commit_command(delete_all_values)

    updated_silver_values = f"""
        INSERT INTO {nome_schema_extracao}.silver_{nome_tabela}
        SELECT word, length::int,category,language
        FROM {nome_schema_extracao}.staging_{nome_tabela};
    """
    cursor_commit_command(updated_silver_values)
else:
    create_table_silver = f"""
        CREATE TABLE {nome_schema_extracao}.silver_{nome_tabela} AS
        SELECT * FROM {nome_schema_extracao}.staging_{nome_tabela}
    """
    cursor_commit_command(create_table_silver)

    change_var_names_layer_silver = f"""
        ALTER TABLE {nome_schema_extracao}.silver_{nome_tabela}
        RENAME COLUMN word TO palavra;

        ALTER TABLE {nome_schema_extracao}.silver_{nome_tabela}
        RENAME COLUMN length TO tamanho_palavra;

        ALTER TABLE {nome_schema_extracao}.silver_{nome_tabela}
        RENAME COLUMN category TO categoria;

        ALTER TABLE {nome_schema_extracao}.silver_{nome_tabela}
        RENAME COLUMN language TO lingua_sigla;
        """
    cursor_commit_command(change_var_names_layer_silver)
    print("MUDOU O NOME DOS VALORES NA CAMADA SILVER ")

change_silver_layer_columns_values = f"""
    ALTER TABLE {nome_schema_extracao}.silver_{nome_tabela}
    ALTER COLUMN palavra TYPE text USING palavra::text,
    ALTER COLUMN tamanho_palavra TYPE integer USING tamanho_palavra::integer,
    ALTER COLUMN categoria TYPE text USING categoria::text,
    ALTER COLUMN lingua_sigla TYPE text USING lingua_sigla::text;
"""
cursor_commit_command(change_silver_layer_columns_values)
print("ALTEROU TIPAGEM DA COLUNA SILVER")

lower_case_silver_layer_values = f"""
    UPDATE {nome_schema_extracao}.silver_{nome_tabela}
    set palavra = lower(palavra),
        categoria = lower(categoria),
        lingua_sigla = lower(lingua_sigla)
"""
cursor_commit_command(lower_case_silver_layer_values)
print("MUDOU TODOS OS VALORES TEXTO PARA LOWERCASE")



##################### TODO CAMADA GOLD ######################################################

check_if_gold_table_exists = check_if_table_exists(nome_schema_extracao,f"gold_{nome_tabela}")

if check_if_gold_table_exists:
    delete_all_values = f"""
        TRUNCATE TABLE {nome_schema_extracao}.gold_{nome_tabela}
    """
    cursor_commit_command(delete_all_values)

    updated_gold_values = f"""
        INSERT INTO {nome_schema_extracao}.gold_{nome_tabela}
        SELECT palavra,tamanho_palavra,categoria,lingua_sigla
        FROM {nome_schema_extracao}.silver_{nome_tabela};
    """
    cursor_commit_command(updated_gold_values)
else:
    create_table_gold = f"""
        CREATE TABLE {nome_schema_extracao}.gold_{nome_tabela} AS
        SELECT * FROM {nome_schema_extracao}.silver_{nome_tabela}
    """
    cursor_commit_command(create_table_gold)

print("ADICIONOU VALORES A CAMADA GOLD")

gold_layer_add_column = f"""
    ALTER TABLE {nome_schema_extracao}.gold_{nome_tabela}
    ADD column if not exists intervalo text
"""
cursor_commit_command(gold_layer_add_column)

update_text_inside = f"""
    UPDATE {nome_schema_extracao}.gold_{nome_tabela}
    SET intervalo = CASE
                    WHEN tamanho_palavra <= 5 THEN 'entre 0 e 5'
                    WHEN tamanho_palavra >= 6 THEN 'entre 6 e 15'
                END;
"""
cursor_commit_command(update_text_inside)

print("ADICIONOU VALOR DE INTERVALO")

############ VIEWS ##################

run_sql_file("sql_queries/vw_duplicadas.sql")
run_sql_file("sql_queries/vw_intervalo.sql")
print("RODOU OS SQLS")
# final
cursor.close()
conn.close()
##