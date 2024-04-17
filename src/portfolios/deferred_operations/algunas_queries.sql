/*
 Query que trae desde credit_cards el card_id, closing_date y due_date y
 de credit_card_operations se trae las repetitions
 */
SELECT
  card_id,
  card_closing_date,
  card_due_date,
  operation_repetitions
FROM
  credit_cards
  INNER JOIN credit_card_operations ON card_id = operation_card_id;

/*
 Query que se trae desde credit_card_operations las repetitions, si es active, el amount y
 desde operation_details se trae el card_id
 hace un inner join con la card id y con la operation id (porque si es solo con la card id 
 trae todos los cruzados que no interesan)
 */
SELECT
  operation_details.operation_card_id,
  operation_repetitions,
  is_active,
  operation_amount
FROM
  credit_card_operations
  INNER JOIN operation_details ON operation_details.operation_card_id = credit_card_operations.operation_card_id
  AND operation_details.operation_id = credit_card_operations.operation_id;

/*
 query que trae: card id, closing date, due date, repetitions, si es active y amount
 se lo trae haciendo un join entre credit_card_operations y operation_details trayendo
 solo la card id (como cc_id), las repetitions, is_active y el amount. A esta tabla la llamo b.
 y joinneo la nueva tabla b con credi_cards en la card_id
 */
SELECT
  card_id,
  card_closing_date,
  card_due_date,
  b.operation_repetitions,
  b.is_active,
  b.operation_amount
FROM
  credit_cards
  INNER JOIN (
    SELECT
      operation_details.operation_card_id AS cc_id,
      operation_repetitions,
      is_active,
      operation_amount
    FROM
      credit_card_operations
      INNER JOIN operation_details ON operation_details.operation_card_id = credit_card_operations.operation_card_id
      AND operation_details.operation_id = credit_card_operations.operation_id
  ) as b ON b.cc_id = credit_cards.card_id;

/*
 Las queries de arriba ya no van más 08/03/2024.
 */
/* Una query para traerme info de UN gasto en particular */
SELECT
  operation_id,
  operation_date,
  operation_time,
  operation_amount,
  installments_payed || '/' || operation_installments as installments,
  installments_amount
FROM
  credit_card_operations
WHERE
  (
    operation_id = 1
    AND operation_card_id = 2455
    AND operation_card_brand = 'VISA'
  );