# %% [markdown]
"""
Northwind Sales Analysis — Script
---------------------------------
This script mirrors the notebook and can be run cell-by-cell in VS Code (look
for the `# %%` markers) or Jupyter. It:

- Extracts order lines from a local MySQL Northwind database into a clean CSV.
- Computes KPIs (monthly revenue, AOV, top customers, top products).
- Produces a set of visuals saved under `figures/`.

Tip: If an editor can’t open `.ipynb`, use this file instead. Logic is the same.
"""

# %% Cell 1 — Install dependencies (optional helper for interactive use)
# If you run this script inside VS Code/Jupyter and need to install packages
# into the current kernel, uncomment the next line and execute this cell.
# %pip install -q pandas==2.2.2 matplotlib==3.9.0 mysql-connector-python==8.4.0

# %% Cell 2 — Robust extract (auto-detects column names; no categories join)
# Goal: connect to MySQL, discover the exact table/column names present in your
# Northwind variant, build a resilient SELECT, and save a tidy CSV of order lines.
#
# Why discovery? Northwind schemas differ (e.g., `order_details` vs `orderdetails`,
# `product_name` vs `productname`). Auto-detection lets this work across variants.
import os
import pandas as pd
import mysql.connector

# Connection settings for your local MySQL instance. Adjust if needed.
HOST = "127.0.0.1"; PORT = 3306; USER = "root"; PASSWORD = "Password"; DB = "northwind"

# Helper: return a dict of {lowercased_column_name: exact_column_name} for a table.
def cols(cur, table):
    cur.execute(f"SHOW COLUMNS FROM {table}")
    return {name.lower(): name for (name, *_) in cur.fetchall()}

# Helper: pick the first candidate name that exists in the given column map.
# If `required=False`, return None when nothing matches instead of raising.
def pick(colmap, candidates, required=True):
    for c in candidates:
        k = c.lower()
        if k in colmap:
            return colmap[k]
    if required:
        raise ValueError(f"Missing any of {candidates}. Have: {sorted(colmap.values())}")
    return None

# Connect to MySQL and list available tables in this schema.
conn = mysql.connector.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB)
cur = conn.cursor()
cur.execute("SHOW TABLES")
tables = {t.lower(): t for (t,) in cur.fetchall()}

# Pick table names
# We support both `order_details` and `orderdetails`.
orders   = tables.get("orders")
orderdet = tables.get("order_details") or tables.get("orderdetails")
products = tables.get("products")
customers = tables.get("customers")  # optional for name later
if not (orders and orderdet and products):
    raise ValueError(f"Expected orders/order_details/products; have: {sorted(tables.values())}")

# Column maps
# Build column dictionaries so we can resolve the exact column names safely.
o_cols  = cols(cur, orders)
od_cols = cols(cur, orderdet)
p_cols  = cols(cur, products)

# Keys and fields (case/variant tolerant)
# Identify join keys and important fields. The `pick` helper makes this robust
# to different naming conventions across Northwind variants.
o_id      = pick(o_cols,  ["orderid","id","order_id"])
o_date    = pick(o_cols,  ["orderdate","order_date","date"])
o_cust_id = pick(o_cols,  ["customerid","customer_id"], required=False)

od_order_id = pick(od_cols, ["orderid","order_id"])
od_prod_id  = pick(od_cols, ["productid","product_id"])
od_price    = pick(od_cols, ["unitprice","unit_price","price"])
od_qty      = pick(od_cols, ["quantity","qty"])
od_disc     = pick(od_cols, ["discount","discount_pct","discount_rate"], required=False)

p_id   = pick(p_cols,  ["productid","id","product_id"])
p_name = pick(p_cols,  ["productname","product_name","name"], required=False)

# Build SELECT fields
# We assemble a list of SQL fields and then join them with ",\n  " for readability.
# `line_total` is computed as UnitPrice * Quantity * (1 - Discount). We use
# `COALESCE` to treat NULL discounts as 0. ProductName is included when present.
fields = [
    f"o.{o_id} AS OrderID",
    f"DATE(o.{o_date}) AS OrderDate",
]
if o_cust_id:
    fields.append(f"o.{o_cust_id} AS CustomerID")
else:
    fields.append("NULL AS CustomerID")

fields += [
    f"od.{od_prod_id} AS ProductID",
    f"od.{od_price} AS UnitPrice",
    f"od.{od_qty} AS Quantity",
]
if od_disc:
    fields.append(f"COALESCE(od.{od_disc}, 0) AS Discount")
    disc_expr = f"COALESCE(od.{od_disc}, 0)"
else:
    fields.append("0 AS Discount")
    disc_expr = "0"

if p_name:
    fields.append(f"p.{p_name} AS ProductName")

select_clause = ",\n  ".join(
    fields + [f"(od.{od_price} * od.{od_qty} * (1 - {disc_expr})) AS line_total"]
)

sql = f"""
SELECT
  {select_clause}
FROM {orders} o
JOIN {orderdet} od ON o.{o_id} = od.{od_order_id}
JOIN {products} p ON od.{od_prod_id} = p.{p_id}
"""

# Note: pandas will emit a warning suggesting SQLAlchemy, but mysql-connector
# works fine here. If desired, you can switch to SQLAlchemy to silence it.
df = pd.read_sql(sql, conn)
conn.close()

# Persist extracted dataset to CSV for portability and repeatable analysis.
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/order_lines.csv", index=False)
len(df)

# %% Cell 3 — KPIs (top customers and top products)
# Goal: load the extracted CSV, compute monthly revenue, Average Order Value
# (AOV), top customers, and top products. These are saved to `data/processed/`
# so plots (and external tools) can consume them easily.
import os
import pandas as pd

df = pd.read_csv("data/processed/order_lines.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df = df.dropna(subset=["OrderDate"])

# Monthly revenue (sum of line totals grouped by calendar month). We group by
# Month Start (MS) so every month aligns to the first day of that month.
monthly = (
    df.groupby(pd.Grouper(key="OrderDate", freq="MS"))["line_total"]
      .sum().reset_index(name="revenue").sort_values("OrderDate")
)

# Average Order Value (AOV) per month: first sum each order’s lines, then take
# the mean across orders in that month.
orders_df = (
    df.groupby(["OrderID", pd.Grouper(key="OrderDate", freq="MS")])["line_total"]
      .sum().reset_index(name="order_value")
)
aov = orders_df.groupby("OrderDate")["order_value"].mean().reset_index(name="aov")

# Top 10 customers by revenue (include NaN customer IDs if present to surface
# anonymous/unknown cases).
top_customers = (
    df.groupby("CustomerID", dropna=False)["line_total"].sum()
      .sort_values(ascending=False).head(10).reset_index()
)

# Top products by revenue (use ProductName if available else ProductID)
by_product = df.groupby(
    (["ProductName"] if "ProductName" in df.columns else ["ProductID"])
)["line_total"].sum().sort_values(ascending=False).reset_index()
top_products = by_product.head(10)

# Save KPI tables to CSV for transparency and reuse.
os.makedirs("data/processed", exist_ok=True)
monthly.to_csv("data/processed/kpi_monthly_revenue.csv", index=False)
aov.to_csv("data/processed/kpi_aov_by_month.csv", index=False)
top_customers.to_csv("data/processed/kpi_top_customers.csv", index=False)
top_products.to_csv("data/processed/kpi_top_products.csv", index=False)

monthly.shape, aov.shape, top_customers.shape, top_products.shape

# %% Cell 4 — Plots (monthly, top customers, top products, distribution)
# Goal: quick visuals that communicate trends and concentration. Images are
# saved to `figures/` so they can be shared or embedded elsewhere.
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

os.makedirs("figures", exist_ok=True)

# Currency/Thousands formatter for axes
currency = FuncFormatter(lambda x, pos: f"${x:,.0f}")

# Monthly revenue
plt.figure(figsize=(8,4))
plt.plot(monthly["OrderDate"], monthly["revenue"], marker="o")
plt.title("Monthly Revenue"); plt.xlabel("Month"); plt.ylabel("Revenue");
ax = plt.gca(); ax.yaxis.set_major_formatter(currency); plt.tight_layout()
plt.savefig("figures/monthly_revenue.png", dpi=150); plt.show()

# Top customers
plt.figure(figsize=(8,4))
plt.barh(top_customers["CustomerID"].astype(str), top_customers["line_total"])
plt.title("Top 10 Customers by Revenue"); plt.xlabel("Revenue");
ax = plt.gca(); ax.xaxis.set_major_formatter(currency); plt.tight_layout()
plt.savefig("figures/top_customers.png", dpi=150); plt.show()

# Top products
label_col = "ProductName" if "ProductName" in by_product.columns else "ProductID"
plt.figure(figsize=(8,4))
plt.barh(top_products[label_col].astype(str), top_products["line_total"])
plt.title("Top 10 Products by Revenue"); plt.xlabel("Revenue");
ax = plt.gca(); ax.xaxis.set_major_formatter(currency); plt.tight_layout()
plt.savefig("figures/top_products.png", dpi=150); plt.show()

# Order value distribution
order_values = df.groupby("OrderID")["line_total"].sum().reset_index(name="order_value")
plt.figure(figsize=(8,4))
plt.hist(order_values["order_value"], bins=20, edgecolor="black")
plt.title("Order Value Distribution"); plt.xlabel("Order Value"); plt.ylabel("Count");
ax = plt.gca(); ax.xaxis.set_major_formatter(currency); plt.tight_layout()
plt.savefig("figures/order_value_distribution.png", dpi=150); plt.show()
