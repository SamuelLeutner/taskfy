INSERT INTO "user" (name, email) VALUES
('Alice', 'alice@example.com'),
('Bruno', 'bruno@example.com'),
('Carla', 'carla@example.com'),
('David', 'david@example.com'); 

INSERT INTO category (category_name) VALUES
('Trabalho'),
('Pessoal'),
('Estudos'),
('Compras'); 

INSERT INTO task (description, user_id_fk, category_id_fk, status) VALUES
('Revisar relatório do TP3', 1, 1, 'Pendente'),   
('Fazer TCC', 1, 3, 'Pendente'),                 
('Ir ao mercado', 2, 2, 'Pendente'),             
('Preparar apresentação', 1, 1, 'Concluída'),    
('Ler livro de Python', 3, 3, 'Pendente');        