Northwind Sales Analysis
================================

A small, reproducible analytics project that extracts order line data from a Northwind MySQL database (or prebuilt CSVs), computes key KPIs, and produces clear visuals. It’s designed to be easy to run for reviewers while also showing the end‑to‑end ETL steps.

Overview
--------------------------------
- Problem: turn raw transactional data into monthly revenue trends, AOV, top customers, and top products — plus a few extra exploratory charts.
- Approach: robust SQL extraction from MySQL to a clean CSV; Pandas for KPIs; Matplotlib for plots. Cells are organized so the visuals can run even without a database.
- Deliverables: processed CSVs in `data/processed/` and PNG figures in `figures/`.

Data Source
--------------------------------
- Schema/data: official Northwind sample (MySQL). The exact files used are included:
  - `data/db/northwind.sql` (schema)
  - `data/db/northwind-data.sql` (data)
- Setup method used: imported both files in MySQL Workbench (File → Open SQL Script → Execute), which creates a `northwind` schema and loads sample data.

Who It’s For
--------------------------------
- Analysts/engineers who want a quick, clean dataset for revenue KPIs.
- Hiring managers reviewing data skills without having to configure a DB (CSV mode works out of the box once CSVs are generated).
- Anyone who wants a minimal, readable reference for ETL → KPIs → charts.

Repository Contents
--------------------------------
- `northwind_analysis.ipynb` — main notebook (ETL, KPIs, plots; also extra exploratory cells).
- `northwind_analysis.py` — script fallback with the same logic (for editors that don’t open notebooks).
- `data/db/` — Northwind MySQL schema and data SQL files.
- `data/processed/` — generated CSVs (created by the notebook).
- `figures/` — generated PNG charts (created by the notebook).

Requirements
--------------------------------
- Python 3.10+
- Jupyter (VS Code + Jupyter extension or classic Jupyter)
- Python packages:
  - `pandas==2.2.2`
  - `matplotlib==3.9.0`
  - `mysql-connector-python==8.4.0`

You can install them either by running the first cell in the notebook (`%pip install ...`) or via pip:

```
pip install pandas==2.2.2 matplotlib==3.9.0 mysql-connector-python==8.4.0
```

Quick Start (CSV Mode)
--------------------------------
No database is required to view charts if the CSVs are already present.
- Open `northwind_analysis.ipynb` and run from the plotting cells onward.
- Or run the script `northwind_analysis.py` cell by cell in VS Code (look for the `# %%` markers).
- Outputs are saved to `figures/` and `data/processed/`.

If `data/processed/order_lines.csv` does not exist yet, run the ETL cells (Cell 2–3) to create it.

Full Pipeline (DB Mode via MySQL Workbench)
--------------------------------
1. Load the Northwind database locally:
   - Open MySQL Workbench.
   - File → Open SQL Script → select `data/db/northwind.sql` → Execute.
   - File → Open SQL Script → select `data/db/northwind-data.sql` → Execute.
   - This creates schema `northwind` and loads data.
2. Open `northwind_analysis.ipynb` and update connection details if needed (default is below):
   - `HOST="127.0.0.1"`, `PORT=3306`, `USER="root"`, `PASSWORD="Password"`, `DB="northwind"`.
3. Run Cells 1→3 to extract and build CSVs; then run the plotting cells.

Configuration
--------------------------------
- Connection settings live near the top of Cell 2 in the notebook (and in the script).
- The extractor auto‑detects table/column names for common Northwind variants, so you don’t need to edit SQL manually.

Outputs
--------------------------------
- CSVs (created by Cell 2–3):
  - `data/processed/order_lines.csv` — order lines with `OrderDate`, `CustomerID`, `ProductID/ProductName`, `UnitPrice`, `Quantity`, `Discount`, and `line_total`.
  - `data/processed/kpi_monthly_revenue.csv` — monthly revenue.
  - `data/processed/kpi_aov_by_month.csv` — average order value by month.
  - `data/processed/kpi_top_customers.csv` — top customers by revenue.
  - `data/processed/kpi_top_products.csv` — top products by revenue.
- Figures:
  - `figures/monthly_revenue.png`, `figures/top_customers.png`, `figures/top_products.png`, `figures/order_value_distribution.png`
  - Additional exploratory: moving average, Pareto, stacked area, weekday pattern, and baseline forecasts.

Data Dictionary (order_lines.csv)
--------------------------------
- `OrderID` (int): Unique identifier of the order.
- `OrderDate` (date): Order date, normalized to date (no time).
- `CustomerID` (int, nullable): Customer identifier (may be null in some rows).
- `ProductID` (int): Product identifier for the line item.
- `ProductName` (string, optional): Product name when available in the schema.
- `UnitPrice` (decimal): Unit price of the item on this order.
- `Quantity` (numeric): Quantity ordered for the line.
- `Discount` (numeric): Discount rate applied to the line (0–1).
- `line_total` (decimal): Computed as `UnitPrice * Quantity * (1 - Discount)`.

How the CSV Was Created (SQL)
--------------------------------
The extractor builds a `SELECT` based on your actual column names. For the included Northwind schema, it’s equivalent to:

```
SELECT
  o.id AS OrderID,
  DATE(o.order_date) AS OrderDate,
  o.customer_id AS CustomerID,
  od.product_id AS ProductID,
  od.unit_price AS UnitPrice,
  od.quantity AS Quantity,
  COALESCE(od.discount, 0) AS Discount,
  (od.unit_price * od.quantity * (1 - COALESCE(od.discount, 0))) AS line_total,
  p.product_name AS ProductName
FROM northwind.orders o
JOIN northwind.order_details od ON o.id = od.order_id
JOIN northwind.products p ON od.product_id = p.id;
```

This result is saved as `data/processed/order_lines.csv`. KPIs are computed from there using Pandas.

Notes & Limitations
--------------------------------
- The dataset is small and synthetic; forecasts included in the extra cells are simple baselines (naive/seasonal‑naive) intended for illustration.
- If your editor highlights `import mysql.connector` with a warning, ensure your VS Code interpreter matches the Jupyter kernel, or install the packages into that interpreter. The notebook still runs as long as the kernel has the dependencies.

Troubleshooting
--------------------------------
- “Editor could not be opened”: if your IDE won’t open `.ipynb`, use `northwind_analysis.py` which mirrors the notebook and can be executed cell‑by‑cell in VS Code.
- `pandas.read_sql` warning: pandas prefers SQLAlchemy engines, but `mysql-connector-python` works; the warning is informational.
- Connection errors: verify MySQL is running and that `HOST/PORT/USER/PASSWORD/DB` match your local setup.

---
If you want this to be fully self‑contained for reviewers without a database, commit the generated `data/processed/*.csv` files. Then anyone can run the visuals immediately.
