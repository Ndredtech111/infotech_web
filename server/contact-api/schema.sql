-- NDR Infotech contact enquiries
-- Run once in phpMyAdmin (select your database first, then open the SQL tab).

CREATE TABLE IF NOT EXISTS enquiries (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name        VARCHAR(80)  NOT NULL,
  email       VARCHAR(120) NOT NULL,
  phone       VARCHAR(20)  NOT NULL,
  topic       VARCHAR(40)  NOT NULL,
  message     TEXT         NOT NULL,
  ip          VARCHAR(45)  NOT NULL DEFAULT '',
  user_agent  VARCHAR(255) NOT NULL DEFAULT '',
  status      ENUM('new','contacted','closed') NOT NULL DEFAULT 'new',
  PRIMARY KEY (id),
  KEY idx_created (created_at),
  KEY idx_ip_created (ip, created_at),
  KEY idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
