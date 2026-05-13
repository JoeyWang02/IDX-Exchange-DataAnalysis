# %%
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## Week 1 – Monthly Dataset Aggregation
# sold1 = pd.read_csv('CRMLSSold202401.csv')
# sold2 = pd.read_csv('CRMLSSold202402.csv') 
# sold = pd.concat([sold1, sold2])
# 
# #Outputs: 
# 
#   Combined sold transactions dataset 
#   Combined listing data dataset 
# 
# #Skills Learned:
# 
#   Multi-file dataset management 
#   Data aggregation with Pandas 
#   Preparing time-series datasets for analysis 

# %%
# combine data
print("Loading Listed Data...")
#### ?
dtype_dict = {
    'ListAgentEmail': str,
    'BuyerAgencyCompensationType': str,
    'BuyerAgentAOR': str,
    'OriginatingSystemName': str,
    'latfilled': float,
    'lonfilled': float
}
listed_files = glob.glob('CRMLSListing*.csv')
df_listed = pd.concat((pd.read_csv(f, low_memory=False, encoding='latin1') for f in listed_files), ignore_index=True)

print("Loading Sold Data...")
sold_files = glob.glob('CRMLSSold*.csv')
df_sold = pd.concat((pd.read_csv(f, low_memory=False, encoding='latin1') for f in sold_files), ignore_index=True)

print("Data loaded successfully!")

# %%
# check head
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(df_listed.head(3))
    display(df_sold.head(3))

# %%
print(f"Listed row count before filtering: {len(df_listed)}")
print(f"Sold row count before filtering: {len(df_sold)}")

# Filter for Residential properties
print("Filtering for Residential properties...\n")

# Print to check available property types in the raw data
print("Original PropertyTypes in Listed Data:", df_listed['PropertyType'].unique())
print("Original PropertyTypes in Sold Data:", df_sold['PropertyType'].unique())

# Execute the filter (case-insensitive, handles NaN values)
#df_listed = df_listed[df_listed['PropertyType'].str.contains('Residential', case=False, na=False)]
#df_sold = df_sold[df_sold['PropertyType'].str.contains('Residential', case=False, na=False)]

print(f"Listed row count after filtering: {len(df_listed)}")
print(f"Sold row count after filtering: {len(df_sold)}")

df_listed.to_csv('Week1_Combined_Listed.csv', index=False, encoding='utf-8-sig')
df_sold.to_csv('Week1_Combined_Sold.csv', index=False, encoding='utf-8-sig')

# %% [markdown]
# ### Summary - Deliverable – Week 1 
# Submit a .py script that concatenates all monthly files from January 2024 through the most recently 
# completed calendar month into two combined datasets (listings and sold), filters both to PropertyType == 
# ‘Residential’ only, and saves them as new CSVs. Include comments confirming row counts before and 
# after concatenation and before and after the Residential filter. 

# %% [markdown]
# ## Weeks 2–3 – Dataset Structuring and Validation

# %%
# Review: check head
df_listed = pd.read_csv('Week1_Combined_Listed.csv')
df_sold = pd.read_csv('Week1_Combined_Sold.csv')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(df_listed.head(3))
    display(df_sold.head(3))

print(f"Listed rows and columns: {df_listed.shape}")
print(f"Sold rows and columns: {df_sold.shape}")


# %%
# Week 2 EDA Validation Report

# check invalid
print("Listed Data Missing Values:")
display(df_listed.isnull().sum().sort_values(ascending=False).head(10))
#print(df_sold.isnull().sum().sort_values(ascending=False))

print("Sold Data Missing Values:")
display(df_sold.isnull().sum().sort_values(ascending=False).head(10))
#print(df_sold.isnull().sum().sort_values(ascending=False))

# Identify "high-risk" columns with > 90% missing values
def check_missing(df, name):
    missing_pct = df.isnull().mean() * 100
    high_missing = missing_pct[missing_pct > 90]
    print(f"Columns with >90% missing values in {name} Data ---")
    print(f"columns with >90% missing values: {len(high_missing)}")
    display(high_missing)
    cols_to_drop = missing_pct[missing_pct == 100].index.tolist()
    # 2. Drop them all at once
    df_drop = df.drop(columns=cols_to_drop)
    print(f"Automatically dropped {len(cols_to_drop)} columns with == 100% missing data.")
    print(f"shape: {df_drop.shape}")
    return df_drop
    

df_listed=check_missing(df_listed, "Listed")
df_sold=check_missing(df_sold, "Sold")

# Core numerical distribution report (min, max, mean, median, percentiles)
core_metrics = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
print("\n--- Core Numerical Distribution for Sold Data (EDA Report Material) ---")

# describe(percentiles=[...]) automatically calculates all required values
#display(df_sold[core_metrics].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.99]).apply(lambda s: s.apply('{0:.2f}'.format)))

# %%
# Clean Unnamed
#df_listed = df_listed.loc[:, ~df_listed.columns.str.contains('^Unnamed')]
#df_sold = df_sold.loc[:, ~df_sold.columns.str.contains('^Unnamed')]

# Drop empty columns


# transfer date
df_listed['ListingContractDate'] = pd.to_datetime(df_listed['ListingContractDate'], errors='coerce')
df_sold['CloseDate'] = pd.to_datetime(df_sold['CloseDate'], errors='coerce')
df_sold['ListingContractDate'] = pd.to_datetime(df_sold['ListingContractDate'], errors='coerce')

# transfer value
numeric_cols_listed = ['OriginalListPrice', 'ListPrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger']
for col in numeric_cols_listed:
    df_listed[col] = pd.to_numeric(df_listed[col], errors='coerce')

numeric_cols_sold = ['ClosePrice', 'ListPrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger']
for col in numeric_cols_sold:
    df_sold[col] = pd.to_numeric(df_sold[col], errors='coerce')
    
print("Data types converted.")

# %% [markdown]
# ## Deliverable – Weeks 2
# Submit a .py script documenting unique property types found, the filtering logic applied, and a null-count 
# summary table. Include a missing value report flagging any columns above 90% null. Produce a numeric 
# distribution summary (min, max, mean, median, percentiles) for ClosePrice, LivingArea, and 
# DaysOnMarket. Save the filtered dataset as a new CSV. 

# %%
# clean duplicate
df_sold = df_sold.drop_duplicates(subset=['ListingKey'], keep='last')

# Filter outliers (only on sold data)
df_sold = df_sold[df_sold['ClosePrice'] > 10000]
df_sold = df_sold[df_sold['LivingArea'] > 100]

# Fill missing values
df_listed['DaysOnMarket'] = df_listed['DaysOnMarket'].fillna(df_listed['DaysOnMarket'].median())
df_listed['PropertyType'] = df_listed['PropertyType'].fillna('Unknown')

df_sold['DaysOnMarket'] = df_sold['DaysOnMarket'].fillna(df_sold['DaysOnMarket'].median())
df_sold['PropertyType'] = df_sold['PropertyType'].fillna('Unknown')

print(f"Cleaned Sold rows: {len(df_sold)}")

# %%
# Listed features
df_listed['PricePerSqFt'] = df_listed['ListPrice'] / df_listed['LivingArea']
df_listed['PricePerSqFt'] = df_listed['PricePerSqFt'].replace([np.inf, -np.inf], np.nan)
df_listed['ListingContractDate'] = pd.to_datetime(df_listed['ListingContractDate'], errors='coerce')
df_listed['ListYear'] = df_listed['ListingContractDate'].dt.year
df_listed['ListMonth'] = df_listed['ListingContractDate'].dt.month

# Sold features
df_sold['PricePerSqFt'] = df_sold['ClosePrice'] / df_sold['LivingArea']
df_sold['PricePerSqFt'] = df_sold['PricePerSqFt'].replace([np.inf, -np.inf], np.nan)

df_sold['SoldToListRatio'] = df_sold['ClosePrice'] / df_sold['ListPrice']
df_sold['SoldToListRatio'] = df_sold['SoldToListRatio'].replace([np.inf, -np.inf], np.nan)

df_sold['CloseYear'] = df_sold['CloseDate'].dt.year
df_sold['CloseMonth'] = df_sold['CloseDate'].dt.month

print("Features engineered.")

# %%
# text 
df_listed['PropertyType'] = df_listed['PropertyType'].astype(str).str.title().str.strip()
df_listed['City'] = df_listed['City'].astype(str).str.title().str.strip()

df_sold['PropertyType'] = df_sold['PropertyType'].astype(str).str.title().str.strip()
df_sold['City'] = df_sold['City'].astype(str).str.title().str.strip()

print("Text data standardized.")

# %%
# 1. Define the list of key numeric fields for analysis
numeric_fields = [
    'ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 
    'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 
    'DaysOnMarket', 'YearBuilt'
]

# Ensure only existing columns are processed
available_fields = [col for col in numeric_fields if col in df_sold.columns]

# 2. Generate Percentile Summaries
# Including extreme percentiles (1% and 99%) to help identify outliers
print("--- Numeric Distribution Summary (Percentiles) ---")
distribution_summary = df_sold[available_fields].describe(
    percentiles=[0.01, 0.25, 0.5, 0.75, 0.9, 0.99]
)
print("--- Numeric Distribution Summary (Original Data) ---")
display(distribution_summary.apply(lambda s: s.apply('{0:.2f}'.format)))

#drop outliers
df_plot = df_sold.copy()
if 'ClosePrice' in df_plot.columns:
    df_plot = df_plot[df_plot['ClosePrice'] < 50_000_000] 
    
if 'LivingArea' in df_plot.columns:
    df_plot = df_plot[df_plot['LivingArea'] < 100_000]

# 3. Visualization: Histograms and Boxplots
print("\n--- Generating Distribution Plots ---")
sns.set_theme(style="whitegrid")

for col in available_fields:
    # Drop NaNs for the specific column to avoid plotting errors
    plot_data = df_plot[col].dropna()
    
    # Create a figure with two subplots: Boxplot (top) and Histogram (bottom)
    # This layout is the industry standard for identifying outliers vs density
    f, (ax_box, ax_hist) = plt.subplots(
        2, sharex=True, 
        gridspec_kw={"height_ratios": (.15, .85)}, 
        figsize=(10, 6)
    )
    
    # Top plot: Boxplot to highlight extreme outliers (points beyond whiskers)
    sns.boxplot(x=plot_data, ax=ax_box, color='skyblue')
    ax_box.set(xlabel='', title=f'Distribution Review: {col}')
    
    # Bottom plot: Histogram with KDE to show data skewness
    sns.histplot(data = plot_data, bins=50, kde=True, ax=ax_hist, color='navy')
    ax_hist.set(ylabel='Frequency')
    
    plt.tight_layout()
    plt.show()

# 4. Outlier Identification (Interquartile Range Method)
print("\n--- Outlier Detection Report (IQR Method) ---")
for col in available_fields:
    Q1 = df_sold[col].quantile(0.25)
    Q3 = df_sold[col].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds for extreme outliers
    lower_bound = Q1 - 3 * IQR
    upper_bound = Q3 + 3 * IQR
    
    outliers = df_sold[(df_sold[col] < lower_bound) | (df_sold[col] > upper_bound)]
    print(f"{col}: Found {len(outliers)} potential outliers (Outside {lower_bound:.2f}- {upper_bound:.2f})")

# %% [markdown]
# ### Data Quality Insight: Numeric Distribution & Extreme Outlier Analysis (Week 2)
# 
# ## 1. Objective
# The primary goal of this analysis is to identify and quantify extreme outliers within the **IDX Real Estate Dataset**. By isolating these anomalies, we ensure that subsequent market trend analysis and Tableau visualizations remain accurate and are not skewed by data entry errors or non-representative luxury properties.
# 
# ---
# 
# ## 2. Methodology
# We utilized the **Interquartile Range (IQR) Method** with a **3x multiplier** (Tukey's Fences) to identify "Extreme Outliers."
# - **Calculations**:
#     - $IQR = Q3 - Q1$
#     - $Lower\ Bound = Q1 - 3 \times IQR$
#     - $Upper\ Bound = Q3 + 3 \times IQR$
# - **Rationale**: A 3x multiplier is more robust for real estate data than the standard 1.5x, focusing specifically on high-impact anomalies (e.g., $800M+ pricing errors) while preserving legitimate high-end market data where possible.
# 
# ---
# 
# ## 3. Statistical Summary Table (3x IQR Results)
# 
# | Feature | Outlier Count | Lower Bound | Upper Bound | Status |
# | :--- | :--- | :--- | :--- | :--- |
# | **ClosePrice** | 9,101 | -$2,974,000.00 | **$4,068,000.00** | Extreme errors detected |
# | **ListPrice** | 9,366 | -$2,935,000.00 | $4,030,000.00 | Consistent with ClosePrice |
# | **LivingArea** | 7,332 | -1,724.00 sqft | **5,052.00 sqft** | Estates/Mansions flagged |
# | **LotSizeAcres**| 69,702 | -0.42 acres | 0.84 acres | Highly right-skewed |
# | **YearBuilt** | **21** | 1843.00 | **2116.00** | **Critical Logic Error** |
# | **DaysOnMarket**| 16,360 | -126.00 days | 189.00 days | Identifies stale listings |
# 
# ---
# 
# ## 4. Key Findings & Insights
# 
# ### A. Chronological Anomalies (`YearBuilt`)
# - **Finding**: 21 records show a `YearBuilt` reaching as far as **2116**.
# - **Impact**: These "future" dates will invalidate time-series trends and age-based depreciation models.
# - **Action**: These rows must be dropped or corrected to the current year if they represent new construction.
# 
# ### B. Pricing Distribution Skewness
# - **Finding**: The mathematical lower bound for `ClosePrice` is negative (-$2.97M), while the upper bound is ~$4.07M.
# - **Insight**: This confirms a heavy **Right-Skewed** distribution. Previously identified data points (e.g., $750M+) are confirmed as extreme statistical noise far beyond the $4M threshold.
# - **Action**: Implement **Capping (Winsorization)** at the $4.07M mark for aggregate reporting to stabilize mean values.
# 
# ### C. Land Size Sensitivity (`LotSizeAcres`)
# - **Finding**: Nearly 70,000 records are flagged as outliers due to a low upper bound of 0.84 acres.
# - **Insight**: The dataset is heavily concentrated in urban/suburban residential properties. Large rural lots are treated as anomalies by the global model, suggesting a need for market segmentation.
# 
# ---
# 
# ## 5. Proposed Handling Strategy
# 
# 1.  **Data Scrubbing**: Permanently drop records where `YearBuilt > 2026`.
# 2.  **Statistical Capping**: Apply `.clip()` to `ClosePrice` and `ListPrice` using the 3x IQR upper bounds to mitigate the influence of "monster" outliers on KPIs.
# 3.  **Market Segmentation**: For `LotSizeAcres`, consider bifurcating the analysis into "Standard Residential" (< 1 acre) and "Acreage/Ranch" (> 1 acre) to better account for variance.
# 

# %%
# 1. Residential vs. Other Property Type Share
print("--- Property Type Share ---")
prop_share = df_sold['PropertyType'].value_counts(normalize=True) * 100
print(prop_share)

# 2. Median and Average Close Prices
avg_price = df_sold['ClosePrice'].mean()
med_price = df_sold['ClosePrice'].median()
print(f"\n--- Price Metrics ---\nAverage: ${avg_price:,.2f}\nMedian: ${med_price:,.2f}")

# 3. Days on Market (DOM) Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df_sold['DaysOnMarket'].dropna(), bins=50, kde=True, color='green')
plt.title('Distribution of Days on Market')
plt.xlim(0, 200) # Zoom in to see the bulk of data
plt.show()

# 4. Sold Above vs. Below List Price
# Logic: Comparison between ClosePrice and ListPrice
df_sold['PriceDiff'] = df_sold['ClosePrice'] - df_sold['ListPrice']
above_list = (df_sold['PriceDiff'] > 0).mean() * 100
below_list = (df_sold['PriceDiff'] < 0).mean() * 100
at_list = (df_sold['PriceDiff'] == 0).mean() * 100

print(f"\n--- Price Strategy Analysis ---")
print(f"Sold Above List: {above_list:.2f}%")
print(f"Sold Below List: {below_list:.2f}%")
print(f"Sold At List: {at_list:.2f}%")

# 5. Date Consistency Issues
# Check if CloseDate is earlier than ListingContractDate
date_errors = df_sold[df_sold['CloseDate'] < df_sold['ListingContractDate']]
print(f"\n--- Data Integrity Check ---")
print(f"Number of records with CloseDate before ListingDate: {len(date_errors)}")

# 6. Counties with the Highest Median Prices
print(f"\n--- Top 5 Counties by Median Price ---")
# Use CountyOrParish (Standard MLS field name)
county_prices = df_sold.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False)
print(county_prices.head(5))

# %%
import pandas as pd

print("Fetching FRED Mortgage Rates...")

# 1. 获取 FRED 数据
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
# 注意：FRED 原始列名是 observation_date 和 MORTGAGE30US
mortgage = pd.read_csv(url) 
mortgage['observation_date'] = pd.to_datetime(mortgage['observation_date'])

# 2. 重采样为月均值
mortgage['year_month'] = mortgage['observation_date'].dt.to_period('M').astype(str)
mortgage_monthly = mortgage.groupby('year_month')['MORTGAGE30US'].mean().reset_index()

# 统一列名：确保这一列的名字铁定叫 'rate_30yr_fixed'
mortgage_monthly.columns = ['year_month', 'rate_30yr_fixed']

# 3. 准备交易数据的关联键
df_sold['PurchaseContractDate'] = pd.to_datetime(df_sold['PurchaseContractDate'], errors='coerce')
df_listed['ListingContractDate'] = pd.to_datetime(df_listed['ListingContractDate'], errors='coerce')

df_sold['year_month'] = df_sold['PurchaseContractDate'].dt.to_period('M').astype(str)
df_listed['year_month'] = df_listed['ListingContractDate'].dt.to_period('M').astype(str)

# 4. 执行合并 (增加防重运行清理逻辑)
# 如果列已经存在，先删掉它，防止出现 _x, _y 后缀
if 'rate_30yr_fixed' in df_sold.columns:
    df_sold = df_sold.drop(columns=['rate_30yr_fixed'])
if 'rate_30yr_fixed' in df_listed.columns:
    df_listed = df_listed.drop(columns=['rate_30yr_fixed'])

sold_with_rates = df_sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = df_listed.merge(mortgage_monthly, on='year_month', how='left')

# 5. 验证检查
print("\n--- Mortgage Rate Merge Validation ---")
# 打印列名，万一报错我们可以一眼看到现在的列名叫什么
print(f"Current columns in Sold data: {sold_with_rates.columns.tolist()}")

sold_nulls = sold_with_rates['rate_30yr_fixed'].isnull().sum()
listed_nulls = listings_with_rates['rate_30yr_fixed'].isnull().sum()

print(f"Null rate values in Sold Data: {sold_nulls}")
print(f"Null rate values in Listed Data: {listed_nulls}")

# 6. 导出
sold_with_rates.to_csv('enriched_sold_data.csv', index=False)
listings_with_rates.to_csv('enriched_listed_data.csv', index=False)

print("\nSuccess! Files saved.")
display(sold_with_rates[['PurchaseContractDate', 'rate_30yr_fixed']].head())

# %%
# Tableau file
df_listed.to_csv('Week3_Enriched_Listed.csv', index=False, encoding='utf-8-sig')
print("✅ Week3_Enriched_Listed.csv exported successfully.")

df_sold.to_csv('Week3_Enriched_Sold.csv', index=False, encoding='utf-8-sig')
print("✅ Week3_Enriched_Sold.csv exported successfully.")

# %%



