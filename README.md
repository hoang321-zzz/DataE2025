# Data Explorers 2025 — Round 1
### End-to-End Business Analytics for a Vietnamese B2B IT Distributor

> **Period:** Jan 1 – Dec 31, 2024 (366 days) · **3 Branches:** Da Nang · Ho Chi Minh City · Hanoi · **4 Product Groups:** Software · Computers · Services · Accessories

---

## Business Overview

| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| **Total Revenue** | 1,034.1B VND | ~1,040B VND | Miss by 0.56% |
| **Total Transactions** | 9,994 | — | — |
| **Gross Profit** | 344.7B VND | — | Stable 33.3% margin |
| **Average Order Value** | 105,481,218 VND | — | Confirms B2B profile |
| **Active Customers** | 168 / 786 SAM | — | 618 untapped prospects |

> A **constant 33.3% gross margin** reflects consistent category-level pricing. An AOV of 105M VND confirms a **pure B2B model** — large, recurring, contract-driven transactions.

---

## Dataset

| File | Description | Role |
|------|-------------|------|
| [`dulieubanhang.csv`](dulieubanhang.csv) | Sales transaction records 2024 | Source of truth |
| [`khachhang.csv`](khachhang.csv) | Customer info & type (Corporate / Retail) | Segmentation base |
| [`sanpham.csv`](sanpham.csv) | Product catalog & product groups | Revenue classification |
| [`nhanvien.csv`](nhanvien.csv) | Sales staff list | Individual performance |
| [`chinhanh.csv`](chinhanh.csv) | Branch information | Geographic analysis |
| [`KPI.csv`](KPI.csv) | Monthly revenue KPI targets per branch | Actual vs. target tracking |

**Data Quality:** [`duplicate.sql`](duplicate.sql) handles deduplication via `ROW_NUMBER() OVER PARTITION BY` across all transactional fields — retaining the lowest `Order ID` per duplicate group.

---

## Revenue by Branch & Product

### Revenue Mix

| Branch | Software | Accessories | Computers | Services | **Total** |
|--------|----------|----------|-----------|-------------|-----------|
| **HCM** | 194B | 97B | 52B | 9B | **~352B VND** |
| **HN** | 189B | 86B | 59B | 8B | **~342B VND** |
| **DN** | 188B | 106B | 43B | 4B | **~341B VND** |

**Key insight:** All three branches generate nearly identical revenue (~1/3 each). **Software accounts for ~55% of total revenue** — the undisputed revenue source. HCM leads overall; Da Nang stands out in Accessories (106B vs. 86–97B at other branches).

### Transaction Volume

| Branch | Software | Accessories | Computers | Services | **Total** |
|--------|----------|----------|-----------|-------------|-----------|
| **DN** | 2,372 | 834 | 166 | 21 | **3,393** |
| **HN** | 2,262 | 845 | 189 | 26 | **3,322** |
| **HCM** | 2,261 | 831 | 165 | 27 | **3,284** |

### Monthly Revenue Trend

```
Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec
 77B   76.9B   95B  90.7B  102.3   88.9B   87.3B    90.6B   89.5B   82.3B   80.3B   72.7B
```

**May is the peak** (102.3B), driven by mid-year corporate budget cycles. **December is the trough** (72.7B), with Jan–Feb also soft (Tet holiday + new fiscal-year lag). The steady Q4 slide signals the need for an **end-of-year deal push** targeting corporate budget flush.

### KPI vs. Actual — [`kpi.sql`](kpi.sql)

Compares actual revenue against monthly KPI targets per branch using `percent_of_kpi`. Full-year gap is only **-0.56%** — very close to target — but low-season months (Jan, Feb, Dec) warrant closer monitoring and pre-emptive campaigns.

---

## Customer Analytics

### 1. RFM Segmentation — [`rfm.py`](rfm.py) · Output: [`khachhang_rfm.csv`](khachhang_rfm.csv)

Segments all **786 customers** across **Recency · Frequency · Monetary** using 5-quantile (1–5) scoring. Segment-level economics below are computed directly from [`customer_value.csv`](customer_value.csv), sorted by revenue contribution:

| Segment | Customers | Revenue (B VND) | % Rev | Cum. % | Avg AOV | Avg Recency | Avg Freq |
|---------|----------:|----------------:|------:|-------:|--------:|------------:|---------:|
| **At Risk** | 109 | 214.5 | 20.7% | 20.7% | 149M | 52d | 13.6 |
| **Champions** | 82 | 206.0 | 19.9% | 40.6% | 149M | 7d | 17.2 |
| **Loyal** | 64 | 141.3 | 13.7% | 54.3% | 155M | 18d | 14.9 |
| **Potential Loyalist** | 147 | 114.9 | 11.1% | 65.4% | 56M | 12d | 14.5 |
| **Need Attention** | 44 | 80.3 | 7.8% | 73.2% | 153M | 15d | 12.4 |
| **Promising** | 60 | 80.2 | 7.8% | 81.0% | 143M | 8d | 9.6 |
| **Cannot Lose Them** | 35 | 79.6 | 7.7% | 88.7% | 228M | 72d | 10.5 |
| **Hibernating** | 90 | 57.3 | 5.5% | 94.2% | 61M | 45d | 10.4 |
| **Lost Customers** | 62 | 20.9 | 2.0% | 96.2% | 41M | 86d | 8.7 |
| **About To Sleep** | 45 | 20.7 | 2.0% | 98.2% | 47M | 29d | 10.8 |
| **New Customers** | 48 | 18.6 | 1.8% | 100.0% | 48M | 12d | 8.1 |
| **Total** | **786** | **1,034.1** | 100% | — | 105M | — | — |

**What the data says:**

1. **🚩 "At Risk" is the #1 revenue segment.** 109 customers (14% of base) generate **214.5B VND — 20.7% of all revenue** — yet their average recency has slipped to **52 days** vs. 7 days for Champions. The single largest revenue block is quietly disengaging; this is the most urgent finding in the analysis.
2. **Champions are the healthy core.** 82 customers, 206B VND, repurchasing every ~7 days at the highest frequency (17.2 orders/yr). Protect and replicate this profile.
3. **Two distinct value tiers by AOV.** Enterprise accounts (At Risk, Champions, Loyal, Need Attention, Promising, Cannot Lose Them) all average **140–230M VND/order**; the volume tier (Potential Loyalist, Hibernating, New, About To Sleep, Lost) sits at **40–61M**. The playbook must differ per tier.
4. **"Cannot Lose Them" = richest baskets, worst recency.** Just 35 accounts but the highest AOV (**228M/order**) and **72 days** since last purchase — small count, outsized value, textbook key-account rescue.
5. **Pareto holds tightly.** Only **6 of 11 segments deliver ~81% of revenue** (the cumulative curve crosses 80% at *Promising*), matching the dashboard Pareto chart exactly.

#### Extended Customer Value — [`customer_value.csv`](customer_value.csv)

Two additional dimensions appended to RFM:
- **AvgOrderValue** = Monetary / Frequency — distinguishes high-spend-few-orders vs. low-spend-many-orders customers
- **TenureMonths** = Time between first and last purchase — long-tenure customers consistently show higher AOV

**Bubble chart insights (AOV × Tenure × Segment):**
- *Cannot Lose Them* — Highest AOV (200M+ VND), moderate tenure → highest revenue risk if churned
- *Champions* — High AOV + long tenure (>10 months) → the **golden tier**
- *Hibernating / Lost* — Low AOV, short tenure → sunk acquisition cost, minimal recovery value

### 2. Cohort Retention — [`cohortanalysis.py`](cohortanalysis.py) · Output: [`cohort_retention_2024.png`](cohort_retention_2024.png)

**Findings:**
- The **January 2024 cohort** (n=513) is unusually large — likely driven by corporate fiscal-year opening orders. Its retention holds flat at **63–67% through month 11**, which is **exceptionally strong** for B2B.
- Smaller cohorts (April–July) show high variance due to small sample size — not statistically reliable.
- Overall pattern: **Flat retention curve after month 1** — once a B2B customer commits, repeat purchasing is stable and predictable.

### 3. Customer Lifetime Value — [`CLV.ipynb`](CLV.ipynb) / [`CLV.py`](CLV.py)

Predicts 6-month CLV using the first 3 months of each customer's transaction history.

**Pipeline:**
1. Remove outliers at the 99th percentile (Revenue & Quantity)
2. Feature engineering: `TotalSpending` and `TotalPurchases` per month (months 0, 1, 2)
3. Target variable: cumulative spend in months 0–5
4. Log-transform target to handle right-skewed revenue distribution

**Model Results (5-fold cross-validation):**

| Model | MAPE | MAE (VND) | Notes |
|-------|------|-----------|-------|
| Linear Regression | 113% | 179M | Baseline — poor |
| Random Forest | 68% | 180M | Improved with log-transform |
| Gradient Boosting | 69% | 183M | Comparable to RF |
| **GBM + RandomizedSearchCV** | **50%** | 215M | Best single model |
| **GBM Ensemble (avg 5 folds)** | **40%** | 166M | **Best overall** |

> **CLV conclusion:** With only one year of data and a limited customer base, MAPE of 40% is acceptable for a B2B setting with large, irregular AOVs. The **Gradient Boosting Ensemble** is the production-ready choice.

**Optimal hyperparameters (GridSearchCV):**
```
learning_rate: 0.1  |  max_depth: 3  |  max_features: log2
min_samples_leaf: 4  |  min_samples_split: 10  |  n_estimators: 50
```

---

## Sales Performance — [`nhanvien.csv`](nhanvien.csv)

> Computed directly from [`dulieubanhang.csv`](dulieubanhang.csv): **249 active sales reps**, 9,994 orders, 1,034.1B VND.

### It's a broad, even sales force — not a star system

| Metric | Value |
|--------|-------|
| Active reps | 249 |
| Revenue / rep | mean **4.15B**, median **3.69B** |
| Orders / rep | mean **40**, median **40** |
| Top earner (NV168) | 11.68B — only **2.8×** the median |
| Top-10 reps' combined share | **9.7%** of revenue |

Revenue is distributed remarkably evenly — the best rep earns under 3× the median, and the entire top 10 accounts for less than 10% of sales. **Upside:** no key-person risk; losing any single rep barely dents revenue. **Downside:** no elite tier drives outsized growth, so scaling today means adding headcount rather than leveraging stars.

### Top 10 earners

| # | Rep | Revenue (B VND) | Orders | AOV (M VND) | Leading product mix |
|--:|-----|----------------:|-------:|------------:|---------------------|
| 1 | **NV168** | 11.68 | 51 | 229 | Accessories 74%, Software 25% |
| 2 | **NV015** | 11.50 | 46 | 250 | Software 64%, Accessories 22% |
| 3 | **NV004** | 11.09 | 44 | 252 | Accessories 48%, Computers 31% |
| 4 | **NV173** | 10.87 | 49 | 222 | Accessories 66%, Software 17% |
| 5 | **NV037** | 10.15 | 52 | 195 | Accessories 75%, Computers 13% |
| 6 | NV170 | 9.77 | 45 | 217 | — |
| 7 | NV125 | 9.67 | 40 | 242 | — |
| 8 | NV038 | 8.78 | 40 | 220 | — |
| 9 | NV093 | 8.65 | 47 | 184 | — |
| 10 | NV147 | 8.60 | 45 | 191 | — |

### Two winning archetypes

- **Big-deal closers** win on order size, not count. **NV168 (#1)** and **NV015 (#2)** post AOVs of **229–250M/order** — more than double the ~105M company average. NV168's entire year is defined by **December: 6.29B from just 3 orders (~2.1B each)** — a single enterprise mega-deal that vaulted them to #1.
- **Volume leaders** win on order count. **NV037** handles the most orders of any top earner (52) at a lower 195M AOV. Pure-volume reps outside the revenue top 10 — NV157 (65 orders), NV190 (62) — move even more transactions but at 60–95M AOV, landing only mid-pack on revenue.

### Top earners over-index on Accessories — a notable contrast

Company-wide, **Software drives 55% of revenue** (69% of all order lines). Yet **4 of the top 5 earners are Accessories-led (66–75%)**. Accessories is the #2 category overall and clearly where the largest individual books are built — worth investigating whether it's higher-margin, bundle-driven, or tied to specific key accounts, then codifying that into the sales playbook.

| Product group | Revenue | Share | Order lines | Share |
|---------------|--------:|------:|------------:|------:|
| Software | 571.0B | 55.2% | 6,896 | 69.0% |
| Accessories | 289.0B | 27.9% | 2,510 | 25.1% |
| Computers | 153.6B | 14.9% | 520 | 5.2% |
| Services | 20.5B | 2.0% | 74 | 0.7% |

Software leads **every month** in both revenue and volume; Services is negligible (2% of revenue, <1% of orders) — a potential whitespace if it carries strategic or margin value worth expanding.

---

## Market Penetration

| Metric | Value | Meaning |
|--------|-------|---------|
| **SAM** | 786 customers | Total serviceable addressable market |
| **SOM** | 168 customers | Currently being served |
| **Earlyvangelists (EVG)** | 82 customers | Most potential customers |
| **Penetration rate** | **10.4%** | 618 prospects still untapped |

> **The single largest growth opportunity:** With only 10.4% SAM penetration, the expansion runway is substantial — especially within the existing database of *At Risk* and *Potential Loyalist* customers who already know the brand.

---

## Business Recommendations

Eight data-grounded actions spanning **every lever** — revenue, margin, sales force, customers, and analytics — ordered by priority (🔴 now · 🟡 this quarter · 🟢 strategic).

| # | Lever | Key finding (from data) | Recommended action |
|--:|-------|-------------------------|--------------------|
| 1 🔴 | **Revenue at risk** | *At Risk* is the **#1 revenue segment** — 214.5B (20.7%) — with recency slipping to 52 days | Launch renewal/upgrade outreach now; recovering just 20% protects **~43B VND** |
| 2 🔴 | **Key accounts** | *Cannot Lose Them* — 35 accounts, richest baskets (228M AOV), 72 days idle, **79.6B exposed** | Assign dedicated account managers — personal contact, not email blasts |
| 3 🟡 | **Sales force** | 249 reps, very flat (top-10 = only 9.7%); volume reps close at **60–95M AOV** vs. closers at **229–250M** | Coach the mid-tier on the big-deal playbook — a small AOV lift across 249 reps compounds enormously |
| 4 🟡 | **Profit margin** | Gross margin is structurally **fixed at 33.3%** across all product groups | Margin can't be moved by mix/pricing — grow gross profit via **revenue scale & lower cost-to-serve** (watch low-AOV, many-line reps) |
| 5 🟡 | **Market growth** | Only **10.4% SAM penetration** (618 prospects untapped); *Potential Loyalist* (147) buys often but at just **56M AOV** | Build an ICP from Champions/Loyal to target the 618; cross-sell Computers/Software to lift baskets |
| 6 🟢 | **Seasonality & KPI** | Full-year **−0.56% vs KPI**; **December is the trough** (72.7B), Jan–Feb soft (77B) | Pull enterprise budget-flush deals into Q4 and pre-load Q1 pipeline to smooth the curve |
| 7 🟢 | **Product focus** | Software 55% + Accessories 28% = **83% of revenue**; Services only 2% | Double down on Software+Accessories bundles (where top earners already win); reassess if Services is worth scaling |
| 8 🟢 | **Predictive analytics** | CLV **GBM Ensemble, MAPE 40%** | Score new customers at month 3; auto-route high-CLV accounts to senior reps early |

**Sequencing:** #1–2 defend the **~294B VND** already at risk (highest ROI — act now) → #3–5 unlock new growth this quarter → #6–8 build durable structural advantage.

---

## Tech Stack & Pipeline

```
SQL Server ──→ Python (pandas, sklearn) ──→ Power BI
     │                   │
     │           rfm.py ──────────→ khachhang_rfm.csv
     │           cohortanalysis.py → cohort_retention_2024.png
     │           CLV.ipynb ─────→ model evaluation
     │
     └── kpi.sql       (KPI vs. Actual)
         cohort.sql    (Cohort pivot table)
         duplicate.sql (Data deduplication)
```

| Layer | Tool | Purpose |
|-------|------|---------|
| Storage | SQL Server | Raw data storage & querying |
| Processing | Python · pandas · scikit-learn | RFM, Cohort, CLV modeling |
| Visualization | Power BI ([`DataE.pbix`](DataE.pbix)) | 3-page dashboard: Overview · Sales Performance · Customer |
| Exploration | Jupyter ([`eda.ipynb`](eda.ipynb) · [`CLV.ipynb`](CLV.ipynb)) | EDA & model experiments |

---

## Setup

```bash
git clone <repo-url>
cd DataExplorers
pip install -r requirements.txt

# Windows
copy .env.example .env
# Fill in SQL Server connection details
```

**`.env`**
```
DB_SERVER=your_server_name
DB_NAME=your_database_name
DB_DRIVER={ODBC Driver 17 for SQL Server}
```

```bash
# Run analyses
python rfm.py             # → khachhang_rfm.csv, customer_value.csv
python cohortanalysis.py  # → cohort_retention_2024.png
jupyter notebook CLV.ipynb
```

---

## Repository Structure

```
DataExplorers/
├── dulieubanhang.csv          # Raw transactions
├── khachhang.csv              # Customer master
├── sanpham.csv                # Product catalog
├── nhanvien.csv               # Sales staff
├── chinhanh.csv               # Branch info
├── KPI.csv                    # Monthly KPI targets
│
├── rfm.py                     # RFM + Customer Value analysis
├── cohortanalysis.py          # Cohort retention analysis
├── CLV.py / CLV.ipynb         # CLV prediction models
├── eda.ipynb                  # Exploratory Data Analysis
├── db.py                      # DB connection helper
│
├── kpi.sql                    # KPI vs. Actual query
├── cohort.sql                 # Cohort pivot (SQL version)
├── duplicate.sql              # Data deduplication
│
├── khachhang_rfm.csv          # Output: RFM segments
├── customer_value.csv         # Output: RFM + AOV + Tenure
├── cohort_retention_2024.png  # Output: Cohort heatmap
├── RankRFM.xlsx               # Output: RFM ranking
└── DataE.pbix                 # Power BI dashboard
```
