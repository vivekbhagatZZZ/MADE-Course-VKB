#################################################### FIRST DATASET ############################################################

import io
import os
import zipfile
import requests
import pandas as pd

output_folder = "./MADE-Course-VKB/data"


# Download CSV from URL
csvURL = "https://data.cms.gov/data-api/v1/dataset/87604795-a3e2-4190-9b3a-e39142221fcd/data.csv"

response = requests.get(csvURL)
DF = pd.read_csv(io.StringIO(response.text))

# Keeping Only Useful Columns, Dropping The Rest
columnsToKeep = [  "Brnd_Name", 
                   "Gnrc_Name", 
                   "Tot_Mftr", 
                   "Mftr_Name", 
                   "Tot_Spndng_2022", 
                   "Tot_Dsg_Unts_2022", 
                   "Tot_Clms_2022", 
                   "Tot_Benes_2022", 
                   "Avg_Spnd_Per_Dsg_Unt_Wghtd_2022", 
                   "Avg_Spnd_Per_Clm_2022", 
                   "Avg_Spnd_Per_Bene_2022"]

newColumnNames = { "Brnd_Name": "Brand Name", 
                   "Gnrc_Name" : "Generic Name", 
                   "Tot_Mftr": "Total Manufacturers", 
                   "Mftr_Name": "Manufacturer Name", 
                   "Tot_Spndng_2022": "Total Spending", 
                   "Tot_Dsg_Unts_2022": "Total Dosgae Units", 
                   "Tot_Clms_2022": "Total Claims", 
                   "Tot_Benes_2022": "Total Beneficiaries", 
                   "Avg_Spnd_Per_Dsg_Unt_Wghtd_2022": 
                   "Average Spending Per Dosage Unit", 
                   "Avg_Spnd_Per_Clm_2022": "Average Spending Per Claim", 
                   "Avg_Spnd_Per_Bene_2022": "Average Spending Per Beneficiary"}

DF = DF[columnsToKeep]
DF.rename(columns = newColumnNames, inplace = True)

# Remove Rows Where "Brand Name" contains '*' or '^' To Maintain Uniformity In Data
DF = DF[~DF["Brand Name"].str.contains(r"[\*\^]", regex = True, na = False)]

# Keep Rows Where Cell Only Contains "Overall"
filteredDF = DF[DF["Manufacturer Name"].str.contains("Overall", na = False)]

# Sort The Column "Total Spending" From Large To Small
sortedDF = filteredDF.sort_values(by='Total Spending', ascending = False)

# Save The Result As An Excel File in 'data' folder
outputFile1 = os.path.join(output_folder, "Medicare Part D Data.xlsx")
sortedDF.to_excel(outputFile1, index = False)

#################################################### SECOND DATASET ############################################################

# URL Of The Zip File
zipURL = "https://www.cms.gov/files/zip/nhe-tables.zip"

# Name Of The File To Extract
targetFile = "Table 16 Retail Prescription Drugs Expenditures.xlsx"

# Download The ZIP file
response = requests.get(zipURL)

# Open The ZIP File In Memory
zipFile = zipfile.ZipFile(io.BytesIO(response.content))

# Extract The Specific File
with zipFile.open(targetFile) as file:
    # Read The Excel File And Select The Desired Range
    DF2 = pd.read_excel(file, sheet_name = 0, usecols = "A:I", skiprows = 2, nrows = 27)

DF2.reset_index(drop = True, inplace = True)

# Drop Rows 2 To 4
DF2 = DF2.drop(index=range(0, 4))

# Rename Columns
newestColumnNames = ["Year", 
                    "Total Cost", 
                    "Out of Pocket Cost", 
                    "Total Health Insurance	Coverage" , 
                    "Private Health Insurance Coverage", 
                    "Medicare Coverage", 
                    "Medicaid	Coverage", 
                    "Other Health Insurance Programs Coverage", 
                    "Other Third Party Payers Coverage"]
DF2.columns = newestColumnNames

outputFile2 = os.path.join(output_folder, "Retail Prescription Drugs Expenditure.xlsx")
DF2.to_excel(outputFile2, index = False)