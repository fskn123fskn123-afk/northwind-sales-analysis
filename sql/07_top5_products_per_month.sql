-- Analysis: Top 5 products per month by revenue
-- Demonstrates: ROW_NUMBER() window function with partitioning

USE northwind;

WITH monthly_product AS (
  SELECT
    DATE(DATE_FORMAT(OrderDate, '%Y-%m-01')) AS month_start,
    ProductID,
    ProductName,
    SUM(line_total) AS revenue
  FROM vw_order_lines_enriched
  GROUP BY month_start, ProductID, ProductName
), ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY month_start ORDER BY revenue DESC) AS rn
  FROM monthly_product
)
SELECT month_start, ProductID, ProductName, revenue
FROM ranked
WHERE rn <= 5
ORDER BY month_start, revenue DESC;

