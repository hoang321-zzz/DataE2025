import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from db import get_engine


def load_data():
    engine = get_engine()
    query = """
        SELECT
            bh.[Mã_KH],
            bh.[Ngày_hạch_toán],
            bh.[Đơn_hàng]
        FROM dbo.dulieubanhang bh
        WHERE bh.[Số_lượng_bán] > 0
          AND bh.[Doanh_thu] > 0
          AND bh.[Mã_KH] IS NOT NULL
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df


def build_cohort_retention(df):
    df["Ngày_hạch_toán"] = pd.to_datetime(df["Ngày_hạch_toán"])
    df["OrderMonth"] = df["Ngày_hạch_toán"].dt.to_period("M")

    # Cohort = tháng mua hàng đầu tiên của mỗi khách
    cohort_map = df.groupby("Mã_KH")["OrderMonth"].min().rename("CohortMonth")
    df = df.join(cohort_map, on="Mã_KH")

    # Số tháng kể từ cohort
    df["CohortIndex"] = (df["OrderMonth"] - df["CohortMonth"]).apply(lambda x: x.n)

    # Số khách hàng duy nhất theo cohort + cohort index
    cohort_data = (
        df.groupby(["CohortMonth", "CohortIndex"])["Mã_KH"]
        .nunique()
        .reset_index(name="Customers")
    )

    cohort_pivot = cohort_data.pivot(index="CohortMonth", columns="CohortIndex", values="Customers")

    # Retention rate: chia cho cohort size (tháng 0)
    cohort_size = cohort_pivot[0]
    retention = cohort_pivot.divide(cohort_size, axis=0).round(3)
    return retention, cohort_size, cohort_pivot

def plot_retention(retention, cohort_size, cohort_pivot):
    yticklabels = [
        f"{str(month)}  (n={int(cohort_size[month])})"
        for month in retention.index
    ]

    plt.figure(figsize=(14, 7))
    sns.heatmap(
        retention,
        annot=cohort_pivot,
        fmt=".0f",
        cmap="YlGnBu",
        linewidths=0.5,
        vmin=0,
        vmax=1,
        yticklabels=yticklabels,
        cbar_kws={"label": "Retention Rate"},
    )
    plt.title("Customer Retention Rate by Cohort — 2024", fontsize=14)
    plt.xlabel("Months Since First Purchase")
    plt.ylabel("Cohort Month")
    plt.tight_layout()
    plt.savefig("cohort_retention_2024.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    df = load_data()
    retention, cohort_size, cohort_pivot = build_cohort_retention(df)

    print("=== Cohort Size (số khách hàng mới mỗi tháng) ===")
    print(cohort_size.to_string())
    print("\n=== Retention Rate ===")
    print(retention.to_string())

    plot_retention(retention, cohort_size, cohort_pivot)
