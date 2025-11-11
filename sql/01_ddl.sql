DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS category;

CREATE TABLE "user" (
    id_user SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE category (
    id_category SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE task (
    id_task SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pendente',
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    user_id_fk INT NOT NULL,
    category_id_fk INT NOT NULL,
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id_fk) 
        REFERENCES "user"(id_user),
    
    CONSTRAINT fk_category
        FOREIGN KEY(category_id_fk) 
        REFERENCES category(id_category)
);