import pandas as pd
import numpy as np
import glob

print("Processing Listed Data...")

listed_files = glob.glob('CRMLSListing*.csv')
df_listed = pd.concat((pd.read_csv(f, low_memory=False) for f in listed_files), ignore_index=True)

df_listed = df_listed.loc[:, ~df_listed.columns.str.contains('^Unnamed')]

df_listed['ListingContractDate'] = pd.to_datetime(df_listed['ListingContractDate'], errors='coerce')

numeric_cols_listed = ['OriginalListPrice', 'ListPrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger']
for col in numeric_cols_listed:
    df_listed[col] = pd.to_numeric(df_listed[col], errors='coerce')

df_listed['DaysOnMarket'] = df_listed['DaysOnMarket'].fillna(df_listed['DaysOnMarket'].median())
df_listed['PropertyType'] = df_listed['PropertyType'].fillna('Unknown')

df_listed['PricePerSqFt'] = df_listed['ListPrice'] / df_listed['LivingArea']
df_listed['PricePerSqFt'] = df_listed['PricePerSqFt'].replace([np.inf, -np.inf], np.nan)

df_listed['ListYear'] = df_listed['ListingContractDate'].dt.year
df_listed['ListMonth'] = df_listed['ListingContractDate'].dt.month

df_listed['PropertyType'] = df_listed['PropertyType'].astype(str).str.title().str.strip()
df_listed['City'] = df_listed['City'].astype(str).str.title().str.strip()

df_listed.to_csv('Tableau_Ready_Listed.csv', index=False, encoding='utf-8-sig')
print("Tableau_Ready_Listed.csv exported successfully.")


print("Processing Sold Data...")

sold_files = glob.glob('CRMLSSold*.csv')
df_sold = pd.concat((pd.read_csv(f, low_memory=False) for f in sold_files), ignore_index=True)

df_sold = df_sold.loc[:, ~df_sold.columns.str.contains('^Unnamed')]

df_sold['CloseDate'] = pd.to_datetime(df_sold['CloseDate'], errors='coerce')
df_sold['ListingContractDate'] = pd.to_datetime(df_sold['ListingContractDate'], errors='coerce')

numeric_cols_sold = ['ClosePrice', 'ListPrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger']
for col in numeric_cols_sold:
    df_sold[col] = pd.to_numeric(df_sold[col], errors='coerce')

df_sold = df_sold.drop_duplicates(subset=['ListingKey'], keep='last')
df_sold = df_sold[df_sold['ClosePrice'] > 10000]
df_sold = df_sold[df_sold['LivingArea'] > 100]

df_sold['DaysOnMarket'] = df_sold['DaysOnMarket'].fillna(df_sold['DaysOnMarket'].median())
df_sold['PropertyType'] = df_sold['PropertyType'].fillna('Unknown')

df_sold['PricePerSqFt'] = df_sold['ClosePrice'] / df_sold['LivingArea']
df_sold['PricePerSqFt'] = df_sold['PricePerSqFt'].replace([np.inf, -np.inf], np.nan)

df_sold['SoldToListRatio'] = df_sold['ClosePrice'] / df_sold['ListPrice']
df_sold['SoldToListRatio'] = df_sold['SoldToListRatio'].replace([np.inf, -np.inf], np.nan)

df_sold['CloseYear'] = df_sold['CloseDate'].dt.year
df_sold['CloseMonth'] = df_sold['CloseDate'].dt.month

df_sold['PropertyType'] = df_sold['PropertyType'].astype(str).str.title().str.strip()
df_sold['City'] = df_sold['City'].astype(str).str.title().str.strip()

df_sold.to_csv('Tableau_Ready_Sold.csv', index=False, encoding='utf-8-sig')
print("Tableau_Ready_Sold.csv exported successfully.")