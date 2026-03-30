# 🧪 Ambiente de Testes Unificado — Airflow + Postgres + pgAdmin

Stack completa para desenvolvimento e testes de pipelines, espelhando o ambiente de produção da VM interna.

---

## 📁 Estrutura de pastas

```
airflow-stack/
├── docker-compose.yml          ← Orquestra todos os serviços
├── Dockerfile                  ← Imagem customizada do Airflow
├── .env.example                ← Copie para .env e preencha
├── .env                        ← (Você cria) Variáveis secretas / APIs
│
├── initdb/
│   └── 01_create_airflow_schema.sql  ← Executado automaticamente na 1ª inicialização
│
├── pgadmin/
│   └── servers.json            ← Servidor pré-configurado no pgAdmin
│
├── dags/                       ← Suas DAGs ficam aqui
│   └── Tools/                  ← Módulos/utilitários compartilhados entre DAGs
│
├── plugins/                    ← Plugins custom do Airflow
├── logs/                       ← Logs gerados pelo Airflow (auto)
├── backups/                    ← Backups do Postgres (montado no Airflow)
└── data/                       ← Dados de entrada/saída para pipelines
```

---

## 🚀 Como subir o ambiente

### 1. Pré-requisitos
- Docker Desktop (Windows/Mac) **ou** Docker Engine + Docker Compose (Linux/WSL)
- WSL2 ativado (se estiver no Windows)

### 2. Primeira execução

```bash
# Clone ou copie a pasta airflow-stack para sua máquina

# Crie o .env a partir do exemplo
cp .env.example .env

# Crie as pastas de volume caso não existam
mkdir -p dags/Tools plugins logs backups data pgadmin

# Build + subir todos os containers
docker compose up -d --build
```

### 3. Acompanhar os logs

```bash
# Todos os serviços
docker compose logs -f

# Só o Airflow
docker compose logs -f airflow

# Só o Postgres
docker compose logs -f postgres
```

---

## 🌐 Acessos

| Serviço   | URL                        | Usuário              | Senha  |
|-----------|----------------------------|----------------------|--------|
| Airflow   | http://localhost:8090      | admin                | admin  |
| pgAdmin   | http://localhost:8080      | admin@setup.com      | 4102   |
| Postgres  | localhost:5433             | postgres             | 4102   |

> O pgAdmin já vem com o servidor **DataWarehouse (SETUP)** pré-configurado.  
> Só precisar inserir a senha `4102` na primeira conexão.

---

## 🔌 Comunicação entre serviços (rede interna)

Todos os containers estão na rede `datastack-net`. Dentro dos containers, use:

| De → Para       | Host a usar              | Porta  |
|-----------------|--------------------------|--------|
| Airflow → Postgres | `postgres`            | `5432` |
| pgAdmin → Postgres | `postgres`            | `5432` |
| DAG → Postgres  | `postgres`               | `5432` |

> **Atenção:** de fora dos containers (ex.: DBeaver, psql local), use `localhost:5433`.

---

## 📦 Enviando para produção (VM do analista)

O analista só precisa de **3 coisas** da pasta `airflow-stack/`:

```
airflow-stack/
├── docker-compose.yml
├── Dockerfile
├── .env                    ← preencher com os valores reais de produção
└── initdb/
    └── 01_create_airflow_schema.sql
```

As DAGs e plugins são copiados separadamente para as pastas `dags/` e `plugins/` na VM.

### Passo a passo para o analista subir em produção:

```bash
# 1. Copiar a pasta para a VM
scp -r airflow-stack/ usuario@vm-interna:/caminho/desejado/

# 2. Dentro da VM / WSL, na pasta airflow-stack:
docker compose up -d --build

# 3. Verificar se tudo subiu
docker compose ps
```

---

## 🛑 Comandos úteis

```bash
# Parar tudo (mantém volumes)
docker compose down

# Parar e apagar volumes (reset total — CUIDADO em produção)
docker compose down -v

# Reiniciar um serviço específico
docker compose restart airflow

# Acessar o terminal do container Airflow
docker exec -it airflow bash

# Acessar o terminal do Postgres
docker exec -it setup_datawarehouse psql -U postgres -d SETUP
```

---

## ⚠️ Observações importantes

- O schema `airflow` é criado automaticamente no banco `SETUP` via script em `initdb/`.
- O Airflow só sobe **depois** que o Postgres passa no healthcheck (`pg_isready`).
- O volume `/var/run/docker.sock` é montado para permitir que DAGs disparem containers Docker — mantenha isso apenas se realmente necessário.
- Altere a `AIRFLOW__API__SECRET_KEY` e a `AIRFLOW__API_AUTH__JWT_SECRET` antes de ir para produção.
