Excel Dashboard — Northwind Sales
================================

Quick Links
--------------------------------
- Workbook: `Excel/Excel northwind analysis.xlsx`
- PDF snapshot: `Excel/Excel northwind analysis.pdf`
- Screenshot: `Excel/screenshot.png`

Overview
--------------------------------
An interactive Excel dashboard built on Northwind order lines. It mirrors the key KPIs and visuals from the repo and is designed for quick review by hiring managers who prefer Excel over BI tools.

Business Insights (sample window)
--------------------------------
- Seasonality: revenue rises sharply in March–April, dips in May, partial recovery in June.
- AOV: March shows the highest Average Order Value, indicating larger baskets and/or premium items.
- Concentration: Top‑10 customers contribute the majority of revenue, suggesting a retention focus.
- Weekday pattern: Friday is the strongest sales day; Tuesday is typically lowest.
- Product mix: a few products dominate while most contribute a long tail of smaller sales.

What This Demonstrates
- Practical dashboarding in Excel (slicers, timeline, PivotCharts).
- Strong layout discipline (consistent sizing, alignment, spacing).
- Clean visual design (borderless charts, subtle gridlines/axes, consistent typography).
- Export‑ready delivery (1‑page PDF with margins and centering).

Compatibility
- Built and tested on Microsoft 365 for Windows (modern Ribbon). Works in Excel 2019/2021 as well.

How To Use
--------------------------------
1) Open and interact
- Open the workbook and Enable Editing/Content if prompted.
- Use the OrderDate timeline to change the period.
- Use the Product slicer to focus on categories or items.

2) Refresh data (if you replace the sample)
- Replace the underlying data range/table with your own (Paste Special → Values into the data sheet, or use Data → Get Data → From Text/CSV, then point the PivotCaches to the new table).
- Data → Refresh All to update all pivots, charts, and KPIs.

3) Export to PDF (1 page)
- Page Layout → Margins: Normal (or 0.5").
- Page Layout → Size: A4 or Letter (match preference).
- Set Print Area around the dashboard region.
- File → Print → Scaling: Fit Sheet on One Page; Page Setup → Center on page (Horizontally, optionally Vertically) → Print to PDF.

Layout & Styling Choices
--------------------------------
- Charts are borderless to read as a unified panel. Legends are hidden for single‑series charts.
- Slicer and timeline use a custom borderless style for a modern look.
- Consistent gutter between panels; objects set to “Move but don’t size with cells”.

Recreate / Adjust The Layout 
--------------------------------
1) Prep
- View → Show → Gridlines (optional while laying out).
- Page Layout → Align → Snap to Grid and Snap to Shape (some builds toggle together).
- Page Layout → Selection Pane for easy multi‑select and naming.

2) Make all charts the same size
- Ctrl+click all charts → Chart Format → Size → set identical Height and Width.

3) Align rows and columns
- Top row (two charts) → Page Layout → Align → Align Top.
- Bottom row (two charts) → Align Top.
- Left column (top+bottom) → Align Left.
- Right column (top+bottom) → Align Left (or Align Right — be consistent).

4) Remove borders
- Charts: right‑click → Format Chart Area → Fill & Line → Border: No line. Also set Plot Area → Border: No line. Use Format Painter to apply to all.
- Slicer: Slicer Tools → Options → Slicer Styles → New Slicer Style… → set Border: None for Whole Slicer, Header, and the Item states. Set as default and apply.
- Timeline: Timeline Tools → Options → Timeline Styles → New Timeline Style… → Border: None for Whole Timeline and Header. Set as default and apply.

5) Lock the layout
- For each chart/slicer: Format → Size & Properties → Properties → Move but don’t size with cells.

Known Quirks (and fixes)
--------------------------------
- Align menu often links “Snap to Grid” and “Snap to Shape” (on/off together). Use Align commands and Size/Position numbers for precision.
- View → Show toggles (Gridlines/Headings/Ruler) are disabled while an object is selected. Press Esc, click a cell, then toggle.
- If gridlines don’t appear, the sheet or cells likely have a Fill color; set Fill = No Fill.

Design Decisions (why it looks this way)
--------------------------------
- Borderless charts and custom borderless slicer/timeline styles to create one cohesive panel without heavy boxes.
- Consistent sizing and Ribbon‑only Align commands for reproducible, pixel‑clean layout; objects set to “Move but don’t size with cells” so edits don’t drift visuals.
- Legends removed on single‑series charts, light gray axes/gridlines, and consistent number formats for focus and readability.
- Export tuned for hiring review: one‑page PDF with centered layout so evaluators get a crisp artifact without opening Excel.



