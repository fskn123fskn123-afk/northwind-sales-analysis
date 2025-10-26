-- Analysis: Revenue by weekday (pivot)
-- Demonstrates: conditional aggregation
-- Output: one row with Sun..Sat columns

USE northwind;

SELECT
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 1 THEN line_total END) AS Sun,
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 2 THEN line_total END) AS Mon,
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 3 THEN line_total END) AS Tue,
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 4 THEN line_total END) AS Wed,
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 5 THEN line_total END) AS Thu,
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 6 THEN line_total END) AS Fri,
  SUM(CASE WHEN DAYOFWEEK(OrderDate) = 7 THEN line_total END) AS Sat
FROM vw_order_lines_enriched;

