import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os

# data_path = "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/"

# df_list = []
# for csv_file in os.listdir(data_path):
#   if csv_file.endswith('.csv'):
#     df_list.append(pd.read_csv(data_path + csv_file, encoding='ISO-8859-1'))

# print(df_list)

# importation des données

# CUSTOMERS
print("TABLE CUSTOMERS")
cst_path = "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Customers.csv"

customer = pd.read_csv(cst_path, encoding='ISO-8859-1')

# print(customer.head())


customer = customer.rename(columns={"CustomerKey": "customer_id", "Gender": "gender", "Name": "name", "State Code": "state_code", "State": "state", "Zip Code": "zip_code", "Continent": "continent","Birthday": "birthday"})
print(customer.info())

customer = pd.read_csv(cst_path, encoding='ISO-8859-1')

# DATA
print("TABLE DATA")

dt_path = "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Data_Dictionary.csv"

data = pd.read_csv(dt_path, encoding='ISO-8859-1')


# print(data.head())

data = data.rename(columns={"Table": "table", "Field": "field", "Description": "description"})
print(data.info())

data = pd.read_csv(dt_path, encoding='ISO-8859-1')

# LOAD DATA INFILE 'C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Data_Dictionary.csv'
# INTO TABLE data_dictionary
# FIELDS TERMINATED BY ','
# OPTIONALLY ENCLOSED BY '"'
# LINES TERMINATED BY '\r\n'
# IGNORE 1 ROWS;


# EXCHANGE

print("TABLE EXCHANGE")

exc_path= "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Exchange_Rates.csv"

exchange = pd.read_csv(exc_path, encoding='ISO-8859-1')

# print(exchange.head())

exchange = exchange.rename(columns={"Date": "date", "Currency": "currency", "Exchange": "exchange"})
print(exchange.info())

exchange = pd.read_csv(exc_path, encoding='ISO-8859-1')
# CREATE TABLE exchange_rates ( date DATE, field_name VARCHAR(185), description TEXT);
# LOAD DATA INFILE 'C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Exchange_Rates.csv'
# INTO TABLE exchange_rates
# FIELDS TERMINATED BY ','
# OPTIONALLY ENCLOSED BY '"'
# LINES TERMINATED BY '\r\n'
# IGNORE 1 ROWS;


# PRODUCT

print("TABLE PRODUCT")

prod_path= "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Products.csv"

product = pd.read_csv(prod_path, encoding='ISO-8859-1')

# print(product.head())

product = product.rename(columns={"ProductKey": "product_id", "Product Name": "Product_name", "Brand": "brand", "Color": "color", "Unit Cost USD": "unit_cost_USD", "Unit Price USD": "unit_price_USD", "SubcategoryKey": "subcategory_id","Subcategory": "subcategory", "CategoryKey": "Category_id", "Category":"category"})
print(product.info())

product = pd.read_csv(prod_path, encoding='ISO-8859-1')


# SALES
print("TABLE SALES")

sls_path= "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Sales.csv"

sales = pd.read_csv(sls_path, encoding='ISO-8859-1')

# print(sales.head())

sales = sales.rename(columns={"Order Number": "order_id", "Line Item": "line_itm", "Order Date": "order_Date", "Delivery Date": "delivery_date", "CustomerKey":"customer_id", "StoreKey": "store_id","ProductKey": "product_id", "Quantity" : "qtity", "Currency Code" : "currency_id"})
print(sales.info())

sales = pd.read_csv(sls_path, encoding='ISO-8859-1')


# STORE
print("TABLE STORE")

str_path= "C:/Users/HP/OneDrive/Documents/Bureau/projet_groupe_1/Stores.csv"

store = pd.read_csv(str_path, encoding='ISO-8859-1')

# print(store.head())

store = store.rename(columns={"StoreKey":"store_id","Country": "country","State" : "state","Square Meters": "square_meters","Open Date":"open_date"})
print(store.info())
store = pd.read_csv(str_path, encoding='ISO-8859-1')

#  Verification des valeurs manquantes
print("TABLE CUSTOMERS")

print(customer.isnull().any())

print("TABLE DATA")

print(data.isnull().any())

print("TABLE EXCHANGE")

print(exchange.isnull().any())

print("TABLE PRODUCT")

print(product.isnull().any())

print("TABLE SALES")

print(sales.isnull().any())

print("TABLE STORE")

print(store.isnull().any())

# suppression des lignes avec des valeurs manquantes

# customer
customer.dropna(inplace=True)
customer = customer.dropna()
customer.shape

# sales
sales.dropna(inplace=True)
sales = sales.dropna()
sales.shape

# store
store.dropna(inplace=True)
store = store.dropna()
store.shape

# Verification qu'il n'y a plus de valeurs manquantes
print("TABLE CUSTOMERS")

print(customer.isnull().any())

print("TABLE SALES")

print(sales.isnull().any())

print("TABLE STORE")

print(store.isnull().any())