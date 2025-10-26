-- SQL Showcase — Setup: enriched view + helpful index
-- Requires: MySQL 8+
-- Purpose: Provide a single, consistent source for order-line analytics and
--          add an index that helps date-driven queries.

USE northwind;

-- Recreate the analytics view used by all KPI queries.
DROP VIEW IF EXISTS vw_order_lines_enriched;
CREATE VIEW vw_order_lines_enriched AS
SELECT
  o.id                         AS OrderID,
  DATE(o.order_date)           AS OrderDate,
  o.customer_id                AS CustomerID,
  od.product_id                AS ProductID,
  p.product_name               AS ProductName,
  od.unit_price                AS UnitPrice,
  od.quantity                  AS Quantity,
  COALESCE(od.discount, 0)     AS Discount,
  od.unit_price * od.quantity * (1 - COALESCE(od.discount, 0)) AS line_total
FROM orders o
JOIN order_details od ON od.order_id = o.id
JOIN products p       ON p.id       = od.product_id;

-- Idempotent index creation for faster month-based scans.
-- MySQL doesn’t support CREATE INDEX IF NOT EXISTS directly; emulate it.
SET @idx_exists := (
  SELECT COUNT(*)
  FROM information_schema.statistics
  WHERE table_schema = DATABASE()
    AND table_name   = 'orders'
    AND index_name   = 'idx_orders_order_date'
);
SET @ddl := IF(@idx_exists = 0,
  'CREATE INDEX idx_orders_order_date ON orders(order_date)',
  'SELECT 1');
PREPARE stmt FROM @ddl; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Optional: analyze table stats (safe if permissions allow)
-- ANALYZE TABLE orders, order_details, products;

