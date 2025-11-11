-- 4a) INNER JOIN
SELECT 
    t.description, t.status, u.name AS user_name, c.category_name
FROM 
    task t
INNER JOIN 
    "user" u ON t.user_id_fk = u.id_user
INNER JOIN 
    category c ON t.category_id_fk = c.id_category
WHERE
    t.status = 'Pendente';


-- 4b) LEFT JOIN
SELECT 
    c.category_name,
    COUNT(t.id_task) AS pending_tasks_count
FROM 
    category c
LEFT JOIN 
    task t ON c.id_category = t.category_id_fk AND t.status = 'Pendente'
GROUP BY 
    c.category_name
ORDER BY 
    c.category_name;

-- 4c) RIGHT JOIN
SELECT 
    u.name AS user_name,
    t.description AS task_description
FROM 
    task t
RIGHT JOIN 
    "user" u ON t.user_id_fk = u.id_user
ORDER BY 
    u.name;