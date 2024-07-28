import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os


#                                        importation et vérification des données

# CUSTOMERS
print("TABLE CUSTOMERS")
cst_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Customers.csv"
customer_df = pd.read_csv(cst_path, encoding='ISO-8859-1')
# print(customer.head())
customers = customer_df.rename(columns={"CustomerKey": "customer_id", "Gender": "gender", "Name": "name", "State Code": "state_code", "State": "state", "Zip Code": "zip_code", "Continent": "continent","Birthday": "birthday"})
print(customers.info())
#Verification des valeurs manquantes
print(customers.isnull().any())
# suppression des lignes avec des valeurs manquantes
customers.dropna(inplace=True)
customer = customers.dropna()
customer.shape
# Verification qu'il n'y a plus de valeurs manquantes
print(customer.isnull().any())


# DATA
print("TABLE DATA")
dt_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Data_Dictionary.csv"
data_df = pd.read_csv(dt_path, encoding='ISO-8859-1')
# print(data.head())
data = data_df.rename(columns={"Table": "table", "Field": "field", "Description": "description"})
print(data.info())
#Verification des valeurs manquantes
print(data.isnull().any())


# EXCHANGE
print("TABLE EXCHANGE")
exc_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Exchange_Rates.csv"
exchange_df = pd.read_csv(exc_path, encoding='ISO-8859-1')
# print(exchange.head())
exchange = exchange_df.rename(columns={"Date": "date", "Currency": "currency", "Exchange": "exchange"})
print(exchange.info())
#Verification des valeurs manquantes
print(exchange.isnull().any())


# PRODUCT
print("TABLE PRODUCT")
prod_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Products.csv"
product_df = pd.read_csv(prod_path, encoding='ISO-8859-1')
# print(product.head())
product = product_df.rename(columns={"ProductKey": "product_id", "Product Name": "Product_name", "Brand": "brand", "Color": "color", "Unit Cost USD": "unit_cost_USD", "Unit Price USD": "unit_price_USD", "SubcategoryKey": "subcategory_id","Subcategory": "subcategory", "CategoryKey": "Category_id", "Category":"category"})
print(product.info())
#Verification des valeurs manquantes
print(product.isnull().any())
#product = pd.read_csv(prod_path, encoding='ISO-8859-1')


# SALES
print("TABLE SALES")
sls_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Sales.csv"
sales_df = pd.read_csv(sls_path, encoding='ISO-8859-1')
# print(sales.head())
sales = sales_df.rename(columns={"Order Number": "order_id", "Line Item": "line_itm", "Order Date": "order_Date", "Delivery Date": "delivery_date", "CustomerKey":"customer_id", "StoreKey": "store_id","ProductKey": "product_id", "Quantity" : "qtity", "Currency Code" : "currency_id"})
print(sales.info())
#Verification des valeurs manquantes
print(sales.isnull().any())
# suppression des lignes avec des valeurs manquantes
sales.dropna(inplace=True)
sales = sales.dropna()
sales.shape
# Verification qu'il n'y a plus de valeurs manquantes
print(sales.isnull().any())
#sales = pd.read_csv(sls_path, encoding='ISO-8859-1')


# STORE
print("TABLE STORE")
str_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Stores.csv"
store_df = pd.read_csv(str_path, encoding='ISO-8859-1')
# print(store.head())
store = store_df.rename(columns={"StoreKey":"store_id","Country": "country","State" : "state","Square Meters": "square_meters","Open Date":"open_date"})
print(store.info())
#Verification des valeurs manquantes
print(store.isnull().any())
# suppression des lignes avec des valeurs manquantes
store.dropna(inplace=True)
store = store.dropna()
store.shape
# Verification qu'il n'y a plus de valeurs manquantes
print(store.isnull().any())
#store = pd.read_csv(str_path, encoding='ISO-8859-1')


#exchange = pd.read_csv(exc_path, encoding='ISO-8859-1')
# CREATE TABLE exchange_rates ( date DATE, field_name VARCHAR(185), description TEXT);
# LOAD DATA INFILE 'C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Exchange_Rates.csv'
# INTO TABLE exchange_rates
# FIELDS TERMINATED BY ','
# OPTIONALLY ENCLOSED BY '"'
# LINES TERMINATED BY '\r\n'
# IGNORE 1 ROWS;

# LOAD DATA INFILE 'C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Data_Dictionary.csv'
# INTO TABLE data_dictionary
# FIELDS TERMINATED BY ','
# OPTIONALLY ENCLOSED BY '"'
# LINES TERMINATED BY '\r\n'
# IGNORE 1 ROWS;

# data_path = "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/"

# df_list = []
# for csv_file in os.listdir(data_path):
#   if csv_file.endswith('.csv'):
#     df_list.append(pd.read_csv(data_path + csv_file, encoding='ISO-8859-1'))

# print(df_list)

#                                              FUSION DATA

# Fusionner les DataFrames par la colonne commune 
df_1 = pd.merge(sales, customers, on='customer_id')
df = pd.merge(df_1, product, on='product_id')

# Afficher le résultat
print(df)
df.head()