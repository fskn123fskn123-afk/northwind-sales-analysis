-- KPI: Monthly revenue with contiguous months and 3-mo moving average
-- Demonstrates: CTEs, WITH RECURSIVE, window functions, outer joins
-- Output: month_start (DATE), revenue (DECIMAL), ma3 (DECIMAL)

USE northwind;

WITH RECURSIVE months AS (
  SELECT
    DATE(DATE_FORMAT(MIN(OrderDate), '%Y-%m-01')) AS month_start,
    DATE(DATE_FORMAT(MAX(OrderDate), '%Y-%m-01')) AS max_month
  FROM vw_order_lines_enriched
  UNION ALL
  SELECT DATE_ADD(month_start, INTERVAL 1 MONTH), max_month
  FROM months
  WHERE month_start < max_month
),
monthly AS (
  SELECT DATE(DATE_FORMAT(OrderDate, '%Y-%m-01')) AS month_start,
         SUM(line_total) AS revenue
  FROM vw_order_lines_enriched
  GROUP BY 1
)
SELECT m.month_start,
       COALESCE(t.revenue, 0) AS revenue,
       AVG(COALESCE(t.revenue, 0)) OVER (
         ORDER BY m.month_start
         ROWS 2 PRECEDING
       ) AS ma3
FROM months m
LEFT JOIN monthly t ON t.month_start = m.month_start
ORDER BY m.month_start;

