# Projeto Taskfy (Projeto de Bloco)

Este é o projeto `taskfy`, um gerenciador de tarefas de linha de comando desenvolvido como parte do Projeto de Bloco.  
A aplicação utiliza **Python**, **SQLAlchemy** para ORM e **PostgreSQL** como banco de dados, tudo gerenciado com **Docker Compose** para facilitar o desenvolvimento e a execução.

---

## Funcionalidades

- **Aplicação Interativa:** Um menu (`main.py`) para Adicionar, Listar, **Visualizar Tarefa Única**, Concluir e Deletar tarefas.  
- **Relatórios SQL (TP3):** Um script separado (`run_reports.py`) que executa as consultas SQL complexas (`INNER`, `LEFT`, `RIGHT JOIN`) exigidas pelo TP3.  
- **Carga e Deleção Massiva (TP4):** Um script de automação (`run_batch.py`) que lê arquivos JSON para realizar inserções, atualizações (Upsert) e deleções em lote no banco de dados.
- **Banco de Dados:** PostgreSQL rodando em container Docker.  
- **Visualização de Dados:** Adminer pré-configurado para fácil acesso ao banco.  

---

## Tecnologias Utilizadas

- Python 3.11  
- SQLAlchemy  
- PostgreSQL 16  
- Docker e Docker Compose  
- Adminer  

---

## Como Rodar o Projeto (Guia de Execução)

Siga os passos abaixo para configurar e rodar o ambiente completo na sua máquina.

### Pré-requisitos

- Docker  
- Docker Compose  

---

### 1. Configurar o Ambiente

#### 1.1 Renomeie o `.env-example`

Na raiz do projeto, copie o arquivo de exemplo para criar seu arquivo de ambiente local:

```bash
cp .env-example .env
````

#### 1.2 Edite o `.env`

Abra o arquivo `.env` e **mude o `DB_HOST` para `db`**.
A senha (`DB_PASS`) deve ser a mesma definida no `docker-compose.yml` (no seu caso, `admin`).

Seu `.env` deve ficar assim:

```ini
DB_USER="postgres"
DB_PASS="admin"
DB_HOST="db"
DB_PORT="5432"
DB_NAME="db_taskfy"
```

-----

### 2\. Limpar e Subir os Serviços

Se você já executou o projeto antes ou **adicionou novos arquivos** (como os scripts do TP4), é **necessário** reconstruir as imagens.

```bash
# Para e remove os containers E os volumes de dados antigos (recomendado para resetar o banco)
docker-compose down -v
```

Em seguida, suba os serviços. Este comando irá construir as imagens e iniciar os 3 containers (App, Banco, Adminer) em segundo plano (`-d`):

```bash
docker-compose up --build -d
```

O container do banco executará automaticamente os scripts `01_ddl.sql` e `02_dml.sql`, criando as tabelas e populando os dados iniciais.

-----

## Como Usar a Aplicação

Com os containers rodando, há quatro formas principais de interagir com o projeto:

### 1\. Visualizar o Banco (Adminer)

1.  Acesse `http://localhost:8080`

2.  Use as credenciais abaixo:

      * **Sistema:** `PostgreSQL`
      * **Servidor:** `db` (o nome do serviço no `docker-compose.yml`)
      * **Usuário:** `postgres` (do seu `.env`)
      * **Senha:** `admin` (do seu `.env`)
      * **Banco de dados:** `db_taskfy` (do seu `.env`)

Você verá as tabelas `user`, `category` e `task` já populadas.

-----

### 2\. Rodar os Relatórios do TP3 (Etapas 5–8)

Para executar o script de relatórios SQL (Joins):

```bash
docker-compose exec app python run_reports.py
```

O terminal exibirá os resultados das consultas `INNER`, `LEFT` e `RIGHT JOIN`, formatados como dicionários e listas.

-----

### 3\. Rodar Carga e Deleção Massiva (TP4)

Para executar o script que processa os arquivos JSON de lote:

```bash
docker-compose exec app python run_batch.py
```

Este comando irá:

1.  Ler o arquivo `data/upsert_data.json` e realizar **Upsert** (Inserir se novo, Atualizar se já existe).
2.  Ler o arquivo `data/delete_data.json` e remover as tarefas listadas.
3.  Exibir no terminal a verificação do sucesso das operações.

-----

### 4\. Rodar o Menu Interativo

Para abrir a aplicação principal (`main.py`) e gerenciar tarefas manualmente:

```bash
docker-compose exec app python main.py
```

O menu definido em `src/utils/menu.py` será exibido, permitindo:

  * Adicionar Tarefa
  * Listar Tarefas Pendentes
  * Listar TODAS as Tarefas
  * Marcar Tarefa como Concluída
  * Remover Tarefa
  * Visualizar Tarefa Única
  * Sair

Todas as operações são lidas e salvas diretamente no banco de dados.
