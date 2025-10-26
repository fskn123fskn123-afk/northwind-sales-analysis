-- Analysis: Pareto (80/20) for products by revenue
-- Demonstrates: window functions, running totals, percent of total

USE northwind;

WITH totals AS (
  SELECT ProductID, ProductName, SUM(line_total) AS revenue
  FROM vw_order_lines_enriched
  GROUP BY ProductID, ProductName
), ranked AS (
  SELECT
    ProductID,
    ProductName,
    revenue,
    SUM(revenue) OVER ()                      AS total_revenue,
    SUM(revenue) OVER (ORDER BY revenue DESC) AS running_revenue
  FROM totals
)
SELECT
  ProductID,
  ProductName,
  revenue,
  running_revenue / NULLIF(total_revenue, 0) AS cum_pct,
  CASE WHEN running_revenue / NULLIF(total_revenue, 0) <= 0.80 THEN 'Top 80%'
       ELSE 'Rest' END AS pareto_band
FROM ranked
ORDER BY revenue DESC;

