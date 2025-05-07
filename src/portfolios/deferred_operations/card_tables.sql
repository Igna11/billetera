PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS credit_cards (
  card_id INTEGER PRIMARY KEY CHECK(LENGTH(CAST(card_id AS TEXT)) = 4),
  card_brand TEXT NOT NULL,
  card_issuer TEXT NOT NULL,
  card_expiration TEXT NOT NULL,
  card_closing_date TEXT NOT NULL,
  card_due_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS credit_card_operations (
  operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  operation_date TEXT NOT NULL,
  operation_time TEXT NOT NULL,
  operation_amount REAL NOT NULL,
  operation_category TEXT NOT NULL,
  operation_subcategory TEXT NOT NULL,
  operation_description TEXT NOT NULL,
  other TEXT,
  operation_card_id INT NOT NULL,
  operation_card_brand TEXT NOT NULL,
  operation_installments INT NOT NULL,
  installments_paid INT NOT NULL,
  installments_amount REAL GENERATED ALWAYS AS (operation_amount / operation_installments) NULL,
  is_active INT NOT NULL,
  FOREIGN KEY (operation_card_id) REFERENCES credit_cards (card_id)
);

SELECT
  user_id,
  first_name,
  last_name,
  birthdate,
  gender,
  region,
  email,
  created_at,
  updated_at
FROM
  users
WHERE
  email = asd;