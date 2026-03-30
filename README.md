# <p align = "center"> AUTOMAÇÃO API MEDALHÃO COM AMBIENTE DOCKER, AIRFLOW E PYTHON </p>
# ⚠️ATENÇÃO⚠️:
  - o arquivo .env é feito para testes e não contém nada comprometedor<br>
# REQUISITOS :<br>
  - 🐳 DOCKER
  - 💻 VIRTUALIZAÇÃO ATIVA NA MÁQUINA WINDOWS
  - 🐧 LINUX UBUNTU INSTALADO EM WSL 2
  - 🔗 DOCKER CONFIGURADO PARA LOCALHOST
  - 💨 CONHECIMENTO BÁSICO EM LOGS AIRFLOW
  - 🏦 CONHECIMENTO EM BANCO DE DADOS POSTGRES ( SQL )
  - 👁  VISUALIZADOR DE BANCO DE DADOS( BEEKEEPER ) 

# PASSO A PASSO:
  1 - Abrir o CMD dentro da pasta com os arquivos
  2 - Docker ativo na máquina
  3 - Rodar o seguinte comando : docker compose up 
  4 - Verificar ip local e abrir o AIRFLOW e POSTGRES com seu login e senha configurados
  5 - Rodar o arquivo python no airflow "api_aleatoria_camadas"
  6 - Se tudo der certo, o banco de dados POSTGRES estará preenchido com os seguintes campos:<br>
    <p align = 'center'> 📂 - extracao_palavras_aleatorias</p> <br>
      🥉 - staging_palavras_aleatórias<br>
      🥈 - silver_palavras_aleatórias<br>
      🥇 - gold_palavras_aleatórias<br>
      👁  - vw_aleatorias_duplicadas<br>
      👁  - vw_aleatorias_ocorrencias
