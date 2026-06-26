import pandas as pd
from db import get_engine

def clv_analysis():
    engine = get_engine()

    query = """
        SELECT
            bh.[Mã_KH],
            bh.[Ngày_hạch_toán],
            bh.[Đơn_hàng],
            bh.[Số_lượng_bán],
            bh.[Doanh_thu],
            kh.[Loại_Khách_hàng]
        FROM dbo.dulieubanhang bh
        LEFT JOIN dbo.khachhang kh ON bh.[Mã_KH] = kh.[Mã_KH]
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

df = clv_analysis()

df = df[df['Số_lượng_bán'] > 0]
df = df[df['Doanh_thu'] > 0] #Remove rows with zero or negative revenue, which may indicate returns or data errors
df = df[~df['Mã_KH'].isna()]
df.isna().sum() #To remove rows with missing customer id

Q = df[['Số_lượng_bán', 'Doanh_thu']].quantile(0.99)

# Filter out outliers in the Doanh_thu and Số_lượng_bán column
df = df[~(df['Số_lượng_bán'] > Q["Số_lượng_bán"])]
df = df[~(df['Doanh_thu'] > Q["Doanh_thu"])]

#Import relativedelta to calculate the difference in months between two dates
from dateutil.relativedelta import relativedelta

# Convert Ngày_hạch_toán to datetime
df['Ngày_hạch_toán'] = pd.to_datetime(df['Ngày_hạch_toán'])

df['First_Purchase'] = df.Mã_KH.map(df.groupby("Mã_KH").Ngày_hạch_toán.min().to_dict())

# Calculate the difference in months between the InvoiceDate column and the latest purchase date
def calculate_relative_difference(x):
    diff = relativedelta(x['Ngày_hạch_toán'], x["First_Purchase"])
    return diff.years * 12 + diff.months

df['MonthsSinceFirstPurchase'] = df.apply(calculate_relative_difference, axis=1)

# Group the data by customer and calculate their total spending, total purchases, and latest purchase date
df["Ngày_hạch_toán2"] = df["Ngày_hạch_toán"]
customer_data = df.groupby(['Mã_KH', 'MonthsSinceFirstPurchase']).agg({
    'Doanh_thu': 'sum',
    'Đơn_hàng': 'nunique',
    'Ngày_hạch_toán': 'min',
    'Ngày_hạch_toán2': 'max'
}).reset_index()

# Rename the columns
customer_data.columns = ['CustomerID', "MonthsSinceFirstPurchase", 'TotalSpending', 'TotalPurchases', 'FirstPurchaseDate', 'LatestPurchaseDate']


# The dataset only contains observations in 2024, so we cannot predict the lifetime value accurately.
# However, we can choose a specific period to make our prediction. For instance, we could predict the
# lifetime value for six months based on the first three months of data. To ensure the dataset's validity,
# we should only consider users who made their first purchase at least six months before the last observation.
customer_data = customer_data[((customer_data.LatestPurchaseDate.max() - customer_data.FirstPurchaseDate).dt.days >= 183)]

customer_data = customer_data[['CustomerID', "MonthsSinceFirstPurchase", 'TotalSpending', 'TotalPurchases']]
X = pd.pivot(customer_data[customer_data["MonthsSinceFirstPurchase"] <= 2], index="CustomerID", columns=["MonthsSinceFirstPurchase"]).fillna(0)
# Flatten the MultiIndex columns of X
X.columns = ['_'.join(str(s) for s in col) for col in X.columns.values]

#Predict the total spending in the next 6 months using the total spending in the first 3 months
cltv = customer_data[customer_data["MonthsSinceFirstPurchase"] <= 6].groupby("CustomerID").TotalSpending.sum().rename("cltv")
prepared_data = X.join(cltv)

# Split the data into features (X) and target variable (y)
X = prepared_data.drop("cltv", axis=1).values
y = prepared_data["cltv"].values

#Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Cross-validation

from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, mean_absolute_error
def run_kfold_cv(X, y, model):
    # Initialize the KFold class
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Initialize a list to store the scores
    mse_scores = []
    mae_scores = []
    mape_scores = []

    # Loop through each fold
    for train_index, test_index in kf.split(X):
        # Split the data into training and testing sets
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        model.fit(X_train, y_train)

        # Use the model to make predictions on the testing set
        y_pred = model.predict(X_test)

        # Calculate the mean squared error (MSE) and store it in the list
        mse_scores.append(mean_squared_error(y_test, y_pred))
        # Calculate the mean absolute error (MAE) and store it in the list
        mae_scores.append(mean_absolute_error(y_test, y_pred))
        # Calculate the mean absolute percentage error (MAPE) and store it in the list
        mape_scores.append(mean_absolute_percentage_error(y_test, y_pred))

    # Calculate the average score
    return  sum(mse_scores) / len(mse_scores), sum(mae_scores) / len(mae_scores), sum(mape_scores) / len(mape_scores)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

for model_name, model in [
    ("Linear regression", LinearRegression()),
    ("Random Forest", RandomForestRegressor()),
    ("Gradient Boosting", GradientBoostingRegressor()),
]:
    scores = run_kfold_cv(X_train, y_train, model)
    print("{}: MSE {:.2f}, MAE {:.2f}, MAPE {:.2f}".format(model_name, *scores))