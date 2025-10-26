-- KPI: Top products by revenue
-- Demonstrates: grouping with labels
-- Output: ProductID, ProductName, revenue

USE northwind;

SELECT
  ProductID,
  ProductName,
  SUM(line_total) AS revenue
FROM vw_order_lines_enriched
GROUP BY ProductID, ProductName
ORDER BY revenue DESC
LIMIT 10;

