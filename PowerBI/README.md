Power BI Report — Northwind Sales
=================================

Quick Links
--------------------------------
- PBIX: `PowerBI/NorthWind PowerBI.pbix`
- PDF snapshot: `PowerBI/NorthWind PowerBI.pdf`
- Screenshot: `PowerBI/screenshot.png`

Overview
--------------------------------
A compact Power BI report that turns Northwind order lines into executive KPIs and a couple of focused drill‑downs. It is intentionally small and review‑friendly while demonstrating core modeling and DAX.

Business Insights (sample window)
--------------------------------
- Seasonality: strong March–April vs. early months; softer May with June recovery.
- AOV peaks around March, suggesting larger baskets/high‑margin items.
- Revenue concentration: Top‑10 customers account for most sales; prioritize retention.
- Product mix: a handful of products dominate with a long tail; monitor stock and promos for leaders.

Pages
--------------------------------
- Overview — KPI cards (Sales, AOV, Orders, Customers), Date/Product slicers, Monthly Sales line, Top‑10 Customers and Top‑10 Products.
- Products — Product table (Sales, Quantity, Orders) and Top‑15 Products chart.

Data Model
--------------------------------
- Import mode with data embedded so reviewers can open without configuring a gateway.
- Star‑like model: a dedicated `Date` table (marked as Date table) related 1→* to the fact table (`OrderLines[OrderDate]`).
- Columns: `UnitPrice`, `Quantity`, `Discount`, derived `line_total`.

Key Measures (examples)
--------------------------------
- `Sales := SUMX(OrderLines, OrderLines[UnitPrice] * OrderLines[Quantity] * (1 - OrderLines[Discount]))`
- `Orders := DISTINCTCOUNT(OrderLines[OrderID])`
- `Customers := DISTINCTCOUNT(OrderLines[CustomerID])`
- `AOV := DIVIDE([Sales], [Orders])`
- Optional time intelligence (YTD, MoM%) using the Date table.

How To Run
--------------------------------
1) Open `NorthWind PowerBI.pbix` in Power BI Desktop (current version recommended).
2) Interact on the Overview page (slicers for period and product). Use the “Products” page for deeper inspection.
3) Export: File → Export → PDF or PNG.

Refresh / Point to Your Data (optional)
--------------------------------
- Keep Import mode: Home → Transform data → Power Query to replace the source with your CSV or DB. Then Refresh.
- Or switch to DirectQuery (for MySQL/SQL Server) if demonstrating live connections; update relationships and re‑validate measures.

Design Notes (for reviewers)
--------------------------------
- Minimal visual chrome; consistent fonts; restrained color palette; slicers at the top for predictable filtering behavior.
- Axis and gridline formatting focused on readability; number formats with thousands separators and currency where appropriate.

Design Decisions (why these choices)
--------------------------------
- Import model with embedded data to eliminate setup friction for reviewers; easy open‑and‑use PBIX.
- Dedicated Date table enables proper time intelligence (YTD, MoM%) and avoids implicit date hierarchies.
- Measures (not calculated columns) for `Sales`, `Orders`, `Customers`, and `AOV` keep the model lean and responsive.
- Simplified visuals and a neutral theme align with business dashboards and avoid unnecessary cognitive load.

Changelog
--------------------------------
- 2025‑10‑31: Updated screenshot and documentation links; verified Import model opens without external dependencies.
