# Projeto Taskfy (Projeto de Bloco)

Este é o projeto `taskfy`, um gerenciador de tarefas de linha de comando desenvolvido como parte do Projeto de Bloco.  
A aplicação utiliza **Python**, **SQLAlchemy** para ORM e **PostgreSQL** como banco de dados, tudo gerenciado com **Docker Compose** para facilitar o desenvolvimento e a execução.

---

## Funcionalidades

- **Aplicação Interativa:** Um menu (`main.py`) para Adicionar, Listar, **Visualizar Tarefa Única**, Concluir e Deletar tarefas.  
- **Relatórios SQL (TP3):** Um script separado (`run_reports.py`) que executa as consultas SQL complexas (`INNER`, `LEFT`, `RIGHT JOIN`) exigidas pelo TP3.  
- **Carga e Deleção Massiva (TP4):** Um script de automação (`run_batch.py`) que lê arquivos JSON para realizar inserções, atualizações (Upsert) e deleções em lote no banco de dados.
- **Web Scraping (TP5):** Módulo completo de scraping que extrai dados de páginas web, armazena em banco de dados e gera relatórios com operações de JOIN.
- **Banco de Dados:** PostgreSQL rodando em container Docker.  
- **Visualização de Dados:** Adminer pré-configurado para fácil acesso ao banco.  

---

## Tecnologias Utilizadas

- Python 3.11  
- SQLAlchemy  
- BeautifulSoup4
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
```

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

---

### 2. Limpar e Subir os Serviços

Se você já executou o projeto antes ou **adicionou novos arquivos** (como os scripts do TP5), é **necessário** reconstruir as imagens.

```bash
# Para e remove os containers E os volumes de dados antigos (recomendado para resetar o banco)
docker-compose down -v
```

Em seguida, suba os serviços. Este comando irá construir as imagens e iniciar os 3 containers (App, Banco, Adminer) em segundo plano (`-d`):

```bash
docker-compose up --build -d
```

O container do banco executará automaticamente os scripts `01_ddl.sql`, `02_dml.sql` e `04_scraping_ddl.sql`, criando as tabelas e populando os dados iniciais.

---

## Como Usar a Aplicação

Com os containers rodando, há cinco formas principais de interagir com o projeto:

### 1. Visualizar o Banco (Adminer)

1. Acesse `http://localhost:8080`

2. Use as credenciais abaixo:
   * **Sistema:** `PostgreSQL`
   * **Servidor:** `db` (o nome do serviço no `docker-compose.yml`)
   * **Usuário:** `postgres` (do seu `.env`)
   * **Senha:** `admin` (do seu `.env`)
   * **Banco de dados:** `db_taskfy` (do seu `.env`)

Você verá as tabelas `user`, `category`, `task`, `scraped_page`, `scraped_article` e `scraping_error`.

---

### 2. Rodar os Relatórios do TP3 (Etapas 5–8)

Para executar o script de relatórios SQL (Joins):

```bash
docker-compose exec app python run_reports.py
```

O terminal exibirá os resultados das consultas `INNER`, `LEFT` e `RIGHT JOIN`, formatados como dicionários e listas.

---

### 3. Rodar Carga e Deleção Massiva (TP4)

Para executar o script que processa os arquivos JSON de lote:

```bash
docker-compose exec app python run_batch.py
```

Este comando irá:

1. Ler o arquivo `data/upsert_data.json` e realizar **Upsert** (Inserir se novo, Atualizar se já existe).
2. Ler o arquivo `data/delete_data.json` e remover as tarefas listadas.
3. Exibir no terminal a verificação do sucesso das operações.

---

### 4. Rodar Web Scraping (TP5) - NOVO

Para executar o módulo de web scraping:

```bash
docker-compose exec app python run_scraping.py
```

Este comando oferece as seguintes opções:

1. **Executar Web Scraping**: Coleta dados de páginas web configuradas
2. **Gerar Relatórios**: Exibe estatísticas e análises dos dados coletados
3. **Executar Scraping + Relatórios**: Executa ambos em sequência

**Funcionalidades do Módulo:**
- Web crawling de múltiplas URLs
- Extração de artigos, títulos, autores e conteúdo
- Tratamento robusto de exceções
- Armazenamento de metadados das páginas
- Registro detalhado de erros
- Relatórios com INNER JOIN, LEFT JOIN e agregações
- Estatísticas gerais (total de páginas, artigos, erros)

---

### 5. Rodar o Menu Interativo

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

---

## Estrutura do Projeto

```
taskfy/
├── data/
│   ├── upsert_data.json
│   └── delete_data.json
├── sql/
│   ├── 01_ddl.sql
│   ├── 02_dml.sql
│   ├── 03_queries.sql
│   └── 04_scraping_ddl.sql
├── src/
│   ├── model/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── task.py
│   │   └── scraping_models.py
│   ├── service/
│   │   ├── task_service.py
│   │   ├── reports_service.py
│   │   ├── scraping_service.py
│   │   └── scraping_reports_service.py
│   └── utils/
│       ├── db_session.py
│       └── menu.py
├── main.py
├── run_reports.py
├── run_batch.py
├── run_scraping.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Entrega do Projeto de Bloco

Este projeto consolida todos os TPs desenvolvidos durante o bloco:

- **TP1**: Estrutura básica e CRUD
- **TP2**: Canvas do projeto e modelagem
- **TP3**: Consultas SQL com JOINs
- **TP4**: Operações em lote (Upsert e Deleção)
- **TP5**: Web Scraping com tratamento de exceções
