-- Data Quality Checks
-- Demonstrates: quick sanity checks on ranges, nulls, referential integrity

USE northwind;

-- 1) Null order dates in the analytics view
SELECT COUNT(*) AS null_orderdate_rows
FROM vw_order_lines_enriched
WHERE OrderDate IS NULL;

-- 2) Discount outside [0,1]
SELECT COUNT(*) AS out_of_range_discounts
FROM vw_order_lines_enriched
WHERE Discount < 0 OR Discount > 1;

-- 3) Negative prices/quantities
SELECT
  SUM(CASE WHEN UnitPrice < 0 THEN 1 ELSE 0 END) AS negative_prices,
  SUM(CASE WHEN Quantity  < 0 THEN 1 ELSE 0 END) AS negative_quantities
FROM vw_order_lines_enriched;

-- 4) Orphan details (base tables) — should be zero
SELECT COUNT(*) AS orphan_details_missing_order
FROM order_details od
LEFT JOIN orders o ON o.id = od.order_id
WHERE o.id IS NULL;

SELECT COUNT(*) AS orphan_details_missing_product
FROM order_details od
LEFT JOIN products p ON p.id = od.product_id
WHERE p.id IS NULL;

-- 5) Potential duplicate lines (same order, product, price, discount)
SELECT COUNT(*) AS duplicate_groups
FROM (
  SELECT order_id, product_id, unit_price, COALESCE(discount,0) AS discount, COUNT(*) AS cnt
  FROM order_details
  GROUP BY order_id, product_id, unit_price, COALESCE(discount,0)
  HAVING COUNT(*) > 1
) d;

-- 6) Coverage: how many rows have unknown CustomerID
SELECT
  SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS unknown_customer_rows,
  COUNT(*) AS total_rows
FROM vw_order_lines_enriched;

