import pandas as pd
from db import get_engine

def rfm_analysis():
    engine = get_engine()
    query = """
        SELECT
            bh.[Mã_KH],
            bh.[Ngày_hạch_toán],
            bh.[Đơn_hàng],
            bh.[Doanh_thu],
            kh.[Loại_Khách_hàng]
        FROM dbo.dulieubanhang bh
        LEFT JOIN dbo.khachhang kh ON bh.[Mã_KH] = kh.[Mã_KH]
        WHERE bh.[Doanh_thu] > 0 AND bh.[Mã_KH] IS NOT NULL
    """
    with engine.connect() as conn:
        df_rfm = pd.read_sql(query, conn)
    print(f"Downloaded {len(df_rfm)} rows of data for RFM analysis.")
    return df_rfm

df_rfm = rfm_analysis()
#Date to datetime
df_rfm['Ngày_hạch_toán'] = pd.to_datetime(df_rfm['Ngày_hạch_toán'])

#Select the report date of RFM analysis as the latest date in the dataset + 1 day
report_date = df_rfm['Ngày_hạch_toán'].max() + pd.Timedelta(days=1)

# Calculate RFM
rfm = df_rfm.groupby('Mã_KH').agg(
    Recency       = ('Ngày_hạch_toán', lambda x: (report_date - x.max()).days),
    Frequency     = ('Đơn_hàng', 'nunique'),
    Monetary      = ('Doanh_thu', 'sum'),
    FirstPurchase = ('Ngày_hạch_toán', 'min'),
    LastPurchase  = ('Ngày_hạch_toán', 'max'),
).reset_index()

rfm['AvgOrderValue'] = (rfm['Monetary'] / rfm['Frequency']).round(0).astype(int)
rfm['TenureMonths']  = ((rfm['LastPurchase'] - rfm['FirstPurchase']).dt.days / 30.44).round(1)

print("\nRFM Table:")
print(rfm.head(10))
print(f"\nShape: {rfm.shape}")
print(rfm.describe())

# 5 quantile to calculate RFM Score
# Recency: 1:Smallest (least recent), 5: Largest (most recent)
rfm['R_score'] = pd.qcut(rfm['Recency'],   q=5, labels=[5,4,3,2,1], duplicates='drop')
# Frequency & Monetary: 1: Smallest, 5: Largest
rfm['F_score'] = pd.qcut(rfm['Frequency'], q=5, labels=[1,2,3,4,5], duplicates='drop')
rfm['M_score'] = pd.qcut(rfm['Monetary'],  q=5, labels=[1,2,3,4,5], duplicates='drop')

rfm['RFM_Score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# RFM Score Segment
segment_scores = {
    'Champions':         {'555','554','544','545','454','455','445'},
    'Loyal':             {'543','444','435','355','354','345','344','335'},
    'Potential Loyalist':{'553','551','552','541','542','533','532','531',
                         '452','451','442','441','431','453','433','432',
                         '423','353','352','351','342','341','333','323'},
    'Promising':         {'525','524','523','522','521','515','514','513',
                         '425','424','413','414','415','315','314','313'},
    'New Customers':     {'512','511','422','421','412','411','311'},
    'Need Attention':    {'535','534','443','434','343','334','325','324'},
    'About To Sleep':    {'331','321','312','221','213','231','241','251'},
    'At Risk':           {'255','254','245','244','253','252','243','242',
                         '235','234','225','224','153','152','145','143',
                         '142','135','134','133','125','124'},
    'Cannot Lose Them':  {'155','154','144','214','215','115','114','113'},
    'Hibernating':       {'332','322','233','232','223','222','132','123','122','212','211'},
    'Lost Customers':    {'111','112','121','131','141','151'},
}

segment_map = {score: seg for seg, scores in segment_scores.items() for score in scores}
rfm['Segment'] = rfm['RFM_Score'].map(segment_map).fillna('Other')

# Export RFM data
df_kh = pd.read_csv('khachhang.csv')
df_kh = df_kh.rename(columns={'Mã KH': 'Mã_KH'})

df_kh_rfm = df_kh.merge(
    rfm[['Mã_KH', 'Recency', 'Frequency', 'Monetary', 'R_score', 'F_score', 'M_score', 'RFM_Score', 'Segment']],
    on='Mã_KH',
    how='left'
)

df_kh_rfm.to_csv('khachhang_rfm.csv', index=False, encoding='utf-8-sig')

# Export customer value analysis (RFM + AvgOrderValue + TenureMonths)
customer_value = rfm[['Mã_KH', 'Recency', 'Frequency', 'Monetary',
                       'AvgOrderValue', 'TenureMonths',
                       'R_score', 'F_score', 'M_score', 'RFM_Score', 'Segment']].copy()

customer_value.to_csv('customer_value.csv', index=False, encoding='utf-8-sig')
print(f"\nExported {len(customer_value)} rows to customer_value.csv")




