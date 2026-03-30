# <p align = "center"> AUTOMAÇÃO API MEDALHÃO COM AMBIENTE DOCKER, AIRFLOW E PYTHON </p>
# ⚠️ATENÇÃO⚠️:
  - o arquivo .env é feito para testes e não contém nada comprometedor<br>
# REQUISITOS :<br>
  - 🐳 DOCKER
  - 💻 VIRTUALIZAÇÃO ATIVA NA MÁQUINA WINDOWS
  - 🐧 WSL 2 CONFIGURADO
  - 🔗 DOCKER CONFIGURADO PARA LOCALHOST
  - 💨 CONHECIMENTO BÁSICO EM LOGS AIRFLOW
  - 🏦 CONHECIMENTO EM BANCO DE DADOS POSTGRES ( SQL )
# PASSO A PASSO:
  1 - Entrar no diretório da pasta pelo comando "cd/local-pasta" dentro do cmd ou digitando cmd dentro do endereço da pasta 
  2 - Docker ativo na máquina<br>
  3 - Rodar o seguinte comando : docker compose up<br> 
  4 - Verificar ip local e abrir localhost do AIRFLOW e POSTGRES com seu login e senha configurados<br>
  5 - Rodar o arquivo python no airflow "api_aleatoria_camadas"<br>
  6 - Se tudo der certo, o banco de dados POSTGRES estará preenchido com os seguintes campos:<br><br>
     SCHEMA - 📂 -> extracao_palavras_aleatorias<br>
      TABLE - 🥉 -> staging_palavras_aleatorias<br>
      TABLE - 🥈 -> silver_palavras_aleatorias<br>
      TABLE - 🥇 -> gold_palavras_aleatorias<br>
      VIEW - 👁 -> vw_aleatorias_duplicadas<br>
      VIEW - 👁 -> vw_aleatorias_ocorrencias
