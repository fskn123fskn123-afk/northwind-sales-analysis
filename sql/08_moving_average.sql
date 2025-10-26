-- Analysis: Monthly revenue with 3-month moving average
-- Demonstrates: window frame, ordering over time

USE northwind;

WITH monthly AS (
  SELECT DATE(DATE_FORMAT(OrderDate, '%Y-%m-01')) AS month_start,
         SUM(line_total) AS revenue
  FROM vw_order_lines_enriched
  GROUP BY 1
)
SELECT month_start,
       revenue,
       AVG(revenue) OVER (
         ORDER BY month_start
         ROWS 2 PRECEDING
       ) AS ma3
FROM monthly
ORDER BY month_start;

