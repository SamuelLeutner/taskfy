from sqlalchemy import text
from src.utils.db_session import get_db_session


def get_inner_join_report():
    """
    Busca o relatório de tarefas pendentes com seus usuários e categorias.
    (Etapa 4a: Consulta com INNER JOIN)
    """

    sql_query = text(
        """
        SELECT 
            t.description, t.status, u.name AS user_name, c.category_name
        FROM task t
        INNER JOIN "user" u ON t.user_id_fk = u.id_user
        INNER JOIN category c ON t.category_id_fk = c.id_category
        WHERE t.status = 'Pendente';
    """
    )

    db = get_db_session()
    try:
        return db.execute(sql_query)
    except Exception as e:
        print(f"Erro ao executar INNER JOIN: {e}")
        return None
    finally:
        db.close()


def get_left_join_report():
    """
    Busca o relatório de todas as categorias e a contagem de tarefas pendentes.
    (Etapa 4b: Consulta com LEFT JOIN)
    """

    sql_query = text(
        """
        SELECT 
            c.category_name, COUNT(t.id_task) AS pending_tasks_count
        FROM category c
        LEFT JOIN task t ON c.id_category = t.category_id_fk AND t.status = 'Pendente'
        GROUP BY c.category_name
        ORDER BY c.category_name;
    """
    )

    db = get_db_session()
    try:
        return db.execute(sql_query)
    except Exception as e:
        print(f"Erro ao executar LEFT JOIN: {e}")
        return None
    finally:
        db.close()


def get_right_join_report():
    """
    Busca o relatório de todos os usuários e suas tarefas (se existirem).
    (Etapa 4c: Consulta com RIGHT JOIN)
    """
    sql_query = text(
        """
        SELECT 
            u.name AS user_name, t.description AS task_description
        FROM task t
        RIGHT JOIN "user" u ON t.user_id_fk = u.id_user
        ORDER BY u.name;
    """
    )

    db = get_db_session()
    try:
        return db.execute(sql_query)
    except Exception as e:
        print(f"Erro ao executar RIGHT JOIN: {e}")
        return None
    finally:
        db.close()
