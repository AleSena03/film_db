CREATE TABLE IF NOT EXISTS film (
    id_film INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titolo VARCHAR(255) NOT NULL,  
    titolo_originale VARCHAR(255) DEFAULT NULL,
    anno YEAR DEFAULT NULL,
    durata INT DEFAULT NULL CHECK (durata IS NULL OR durata > 0),
    regia VARCHAR(255) DEFAULT NULL,
    lingua_originale VARCHAR(100) DEFAULT NULL,
    saga VARCHAR(255) DEFAULT NULL,
    id_prequel INT UNSIGNED DEFAULT NULL,
    id_sequel INT UNSIGNED DEFAULT NULL,
    poster VARCHAR(2083) DEFAULT NULL,
    budget BIGINT UNSIGNED DEFAULT NULL CHECK (budget IS NULL OR budget >= 0),
    incasso_primo_weekend_usa BIGINT UNSIGNED DEFAULT NULL CHECK (incasso_primo_weekend_usa IS NULL OR incasso_primo_weekend_usa >= 0),
    incasso_usa BIGINT UNSIGNED DEFAULT NULL CHECK (incasso_usa IS NULL OR incasso_usa >= 0),
    incasso_globale BIGINT UNSIGNED DEFAULT NULL CHECK (incasso_globale IS NULL OR incasso_globale >= 0),
    valutazione_imdb DECIMAL(3,1) DEFAULT NULL CHECK (valutazione_imdb IS NULL OR valutazione_imdb BETWEEN 0 AND 10),
    data_creazione DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_ultima_modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
    FOREIGN KEY(id_prequel) REFERENCES film(id_film) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY(id_sequel) REFERENCES film(id_film) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;