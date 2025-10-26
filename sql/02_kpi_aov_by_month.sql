-- KPI: Average Order Value (AOV) by month
-- Demonstrates: order-level aggregation then monthly average
-- Output: month_start (DATE), aov (DECIMAL)

USE northwind;

WITH order_values AS (
  SELECT OrderID,
         DATE(DATE_FORMAT(OrderDate, '%Y-%m-01')) AS month_start,
         SUM(line_total) AS order_value
  FROM vw_order_lines_enriched
  GROUP BY OrderID, month_start
)
SELECT month_start,
       AVG(order_value) AS aov
FROM order_values
GROUP BY month_start
ORDER BY month_start;

