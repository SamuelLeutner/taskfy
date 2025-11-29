import json
import os
import sys
from sqlalchemy import text
from src.utils.db_session import get_db_session, check_db_connection, init_db
from src.model.task import Task

UPSERT_FILE = "data/upsert_data.json"
DELETE_FILE = "data/delete_data.json"


def load_json(file_path):
    """Lê um arquivo JSON e retorna os dados."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return []
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON {file_path}: {e}")
        return []


def run_upsert():
    """
    Item 3 e 4: Realiza INSERT ou UPDATE (Upsert) massivo.
    """
    print(f"\n>>> Iniciando Processo de UPSERT (Carga Massiva) usando {UPSERT_FILE}")

    data = load_json(UPSERT_FILE)
    if not data:
        return

    db = get_db_session()
    try:
        count_insert = 0
        count_update = 0

        for item in data:
            task_id = item.get("id_task")

            existing_task = None
            if task_id:
                existing_task = db.query(Task).filter(Task.id_task == task_id).first()

            if existing_task:
                print(f"   [UPDATE] Atualizando tarefa ID {task_id}...")
                existing_task.description = item.get(
                    "description", existing_task.description
                )
                existing_task.status = item.get("status", existing_task.status)
                existing_task.user_id_fk = item.get(
                    "user_id_fk", existing_task.user_id_fk
                )
                existing_task.category_id_fk = item.get(
                    "category_id_fk", existing_task.category_id_fk
                )
                count_update += 1
            else:
                print(f"   [INSERT] Criando nova tarefa: {item.get('description')}")
                new_task = Task(
                    description=item.get("description"),
                    status=item.get("status", "Pendente"),
                    user_id_fk=item.get("user_id_fk"),
                    category_id_fk=item.get("category_id_fk"),
                )
                db.add(new_task)
                count_insert += 1

        db.commit()
        print(
            f"Sucesso! {count_update} tarefas atualizadas e {count_insert} tarefas inseridas."
        )

        verify_upsert(db)

    except Exception as e:
        db.rollback()
        print(f"Erro durante o Upsert: {e}")
    finally:
        db.close()


def verify_upsert(db):
    """Verifica e exibe os dados atuais após o Upsert."""
    print("\n--- Verificação pós-Upsert (5 últimas tarefas modificadas/criadas) ---")
    tasks = db.query(Task).order_by(Task.id_task.desc()).limit(5).all()
    for t in tasks:
        print(t)


def run_delete():
    """
    Item 5 e 6: Realiza Deleção massiva.
    """
    print(f"\n>>> Iniciando Processo de DELEÇÃO Massiva usando {DELETE_FILE}")

    data = load_json(DELETE_FILE)
    if not data:
        return

    db = get_db_session()
    try:
        count_deleted = 0

        for item in data:
            task_id = item.get("id_task")
            if not task_id:
                continue

            task_to_delete = db.query(Task).filter(Task.id_task == task_id).first()

            if task_to_delete:
                db.delete(task_to_delete)
                print(f"   [DELETE] Tarefa ID {task_id} removida.")
                count_deleted += 1
            else:
                print(f"   [SKIP] Tarefa ID {task_id} não encontrada para deleção.")

        db.commit()
        print(f"Sucesso! {count_deleted} tarefas removidas.")

        verify_delete(db, data)

    except Exception as e:
        db.rollback()
        print(f"Erro durante a Deleção: {e}")
    finally:
        db.close()


def verify_delete(db, data_attempted):
    """Confere se os IDs realmente sumiram."""
    print("\n--- Verificação pós-Deleção ---")
    ids_to_check = [item["id_task"] for item in data_attempted if "id_task" in item]

    remaining = db.query(Task).filter(Task.id_task.in_(ids_to_check)).all()

    if not remaining:
        print("Confirmação: Nenhum dos IDs deletados foi encontrado no banco.")
    else:
        print(
            f"Atenção: As seguintes tarefas ainda constam no banco: {[t.id_task for t in remaining]}"
        )


def main():
    if not check_db_connection():
        sys.exit(1)

    init_db()

    run_upsert()

    run_delete()


if __name__ == "__main__":
    main()
