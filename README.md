# Projeto Taskfy (Projeto de Bloco)

Este é o projeto `taskfy`, um gerenciador de tarefas de linha de comando desenvolvido como parte do Projeto de Bloco.  
A aplicação utiliza **Python**, **SQLAlchemy** para ORM e **PostgreSQL** como banco de dados, tudo gerenciado com **Docker Compose** para facilitar o desenvolvimento e a execução.

---

## Funcionalidades

- **Aplicação Interativa:** Um menu (`main.py`) para adicionar, listar, concluir e deletar tarefas.  
- **Relatórios SQL:** Scripts (`run_reports.py`) que executam consultas SQL complexas (`INNER`, `LEFT`, `RIGHT JOIN`).  
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
```bash
cp .env-example .env
````

#### 1.2 Edite o `.env`

Abra o arquivo `.env` e **mude o `DB_HOST` para `db`**.
A senha (`DB_PASS`) deve ser a mesma definida no `docker-compose.yml` (ou altere em ambos os locais).

Seu `.env` deve ficar assim:

```ini
DB_USER="postgres"
DB_PASS="admin"
DB_HOST="db"
DB_PORT="5432"
DB_NAME="db_taskfy"
```

---

### 2. Subir os Serviços

Este comando irá construir as imagens e iniciar os 3 containers (App, Banco, Adminer) em segundo plano (`-d`):

```bash
docker-compose up --build -d
```

O container do banco executará automaticamente os scripts `01_ddl.sql` e `02_dml.sql`, criando as tabelas e populando os dados.

---

## Como Usar a Aplicação

Com os containers rodando, há três formas principais de interagir com o projeto:

### 1. Visualizar o Banco (Adminer)

1. Acesse `http://localhost:8080`
2. Use as credenciais abaixo:

   * **Sistema:** PostgreSQL
   * **Servidor:** db
   * **Usuário:** postgres
   * **Senha:** admin
   * **Banco de dados:** db_taskfy

Você verá as tabelas `user`, `category` e `task` já populadas.

---

### 2. Rodar os Relatórios do TP3 (Etapas 5–8)

Para executar o script de relatórios:

```bash
docker-compose exec app python run_reports.py
```

Explicando:

* `docker-compose exec`: executa um comando em um container.
* `app`: nome do serviço onde o comando será executado.
* `python src/utils/run_reports.py`: comando para rodar o script de relatórios.

O terminal exibirá os resultados das consultas `INNER`, `LEFT` e `RIGHT JOIN`.

---

### 3. Rodar o Menu Interativo

Para abrir o menu principal (`main.py`):

```bash
docker-compose exec app python main.py
```

O menu definido em `taskfy/src/utils/menu.py` será exibido, permitindo adicionar, listar, concluir e deletar tarefas — tudo integrado ao banco de dados.
