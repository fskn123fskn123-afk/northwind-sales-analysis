-- KPI: Top N customers by revenue
-- Demonstrates: grouping, parameterization via user variable
-- Edit @limit to change the number of rows returned

USE northwind;

SET @limit := 10; -- change as needed

SELECT
  COALESCE(CAST(CustomerID AS CHAR), 'Unknown') AS CustomerID,
  SUM(line_total) AS revenue
FROM vw_order_lines_enriched
GROUP BY CustomerID
ORDER BY revenue DESC
LIMIT @limit;

