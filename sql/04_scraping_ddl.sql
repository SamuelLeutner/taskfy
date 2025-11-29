-- Tabela de páginas visitadas (metadados)
CREATE TABLE IF NOT EXISTS scraped_page (
    id_page SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL UNIQUE,
    title VARCHAR(255),
    scraping_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_code INTEGER,
    content_length INTEGER
);

-- Tabela de artigos/conteúdos extraídos
CREATE TABLE IF NOT EXISTS scraped_article (
    id_article SERIAL PRIMARY KEY,
    page_id_fk INTEGER NOT NULL,
    title VARCHAR(255),
    author VARCHAR(100),
    publish_date VARCHAR(50),
    content_preview TEXT,
    article_url VARCHAR(500),
    extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_scraped_page
        FOREIGN KEY(page_id_fk)
        REFERENCES scraped_page(id_page)
        ON DELETE CASCADE
);

-- Tabela de erros/exceções durante scraping
CREATE TABLE IF NOT EXISTS scraping_error (
    id_error SERIAL PRIMARY KEY,
    page_id_fk INTEGER,
    url_attempted VARCHAR(500) NOT NULL,
    error_type VARCHAR(100),
    error_message TEXT,
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_error_page
        FOREIGN KEY(page_id_fk)
        REFERENCES scraped_page(id_page)
        ON DELETE SET NULL
);

-- Índices para melhorar performance das consultas
CREATE INDEX IF NOT EXISTS idx_scraped_article_page ON scraped_article(page_id_fk);
CREATE INDEX IF NOT EXISTS idx_scraping_error_page ON scraping_error(page_id_fk);
CREATE INDEX IF NOT EXISTS idx_scraped_article_author ON scraped_article(author);
CREATE INDEX IF NOT EXISTS idx_scraped_page_url ON scraped_page(url);