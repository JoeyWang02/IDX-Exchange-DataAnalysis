import subprocess
import time
import pandas as pd
import glob

print("Running crmls_listed.py for all months from January 2024 to March 2026...")

#for year in range(2024, 2027):
#    for month in range(1, 13):
#        if year == 2026 and month > 3:
#            break
#        print(f"Processing data for {year}-{month:02d}...")
#        #subprocess.run(['python', 'crmls_listed.py', str(year), str(month)])
#        subprocess.run(['python', 'crmls_sold.py', str(year), str(month)])
#        time.sleep(1)  # Add a delay of 1 second between each execution

print("Combine data for all months from January 2024 to March 2026...")

print("Starting to merge Listed data...")
listed_files = glob.glob('CRMLSListing*.csv') 
df_listed = pd.concat((pd.read_csv(f) for f in listed_files), ignore_index=True)

# Save the merged Listed data
print(f"Listed data merged successfully! Total rows: {len(df_listed)}. Exporting...")
df_listed.to_csv('Final_Listed_Data.csv', index=False, encoding='utf-8-sig')
print("Final Listed table saved as Final_Listed_Data.csv")


print("Starting to merge Sold data...")
sold_files = glob.glob('CRMLSSold*.csv')
df_sold = pd.concat((pd.read_csv(f) for f in sold_files), ignore_index=True)

# Save the merged Sold data
print(f"Sold data merged successfully! Total rows: {len(df_sold)}. Exporting...")
df_sold.to_csv('Final_Sold_Data.csv', index=False, encoding='utf-8-sig')
print("Final Sold table saved as Final_Sold_Data.csv")
