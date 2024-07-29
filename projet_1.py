import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ----------------------IMPORTATION DES DONNEES------------------------------
def importation(path):
    return pd.read_csv(path, encoding='ISO-8859-1')


# customers
print("TABLE CUSTOMERS")
cst_path = "datasets/Customers.csv"
customer = importation(cst_path)


# data
print("TABLE DATA")
dt_path = "./datasets/Data_Dictionary.csv"
data = importation(dt_path)


# exchange
print("TABLE EXCHANGE")
exc_path= "./datasets/Exchange_Rates.csv"
exchange = importation(exc_path)


# product
print("TABLE PRODUCT")
prod_path= "./datasets/Products.csv"
product = importation(prod_path)


# sales
print("TABLE SALES")
sls_path= "./datasets/Sales.csv"
sales = importation(sls_path)


# store
print("TABLE STORE")
str_path= "./datasets/Stores.csv"
store = importation(str_path)


# ----------------------RENOMMER LES COLONNES------------------------------

# customer
customer= customer.rename(columns={"CustomerKey": "customer_id", "Gender": "gender", "Name": "name", "City":"cst_city","State Code": "cst_state_code", "State" : "cst_state","Zip Code":"cst_zip_code","Country" : "cst_country","Continent": "cst_continent","Birthday":"cst_birthday"})

# data
data = data.rename(columns={"Date" : "data_date","Currency" : "data_currency", "Exchange":"exchange"})

# exchange
exchange = exchange.rename(columns={"Date": "exchange_date", "Currency":"currency_code", "Exchange":"exchange"})

# product
product = product.rename(columns={"ProductKey": "product_id","Product Name": "product_name","Brand": "brand", "Color": "color", "Unit Cost USD": "unit_cost_USD", "Unit Price USD": "unit_price_USD", "SubcategoryKey": "subcategory_id","Subcategory": "subcategory", "CategoryKey": "category_id", "Category":"category"})

# sales
sales = sales.rename(columns={"Order Number" : "order_number","Line Item" : "line_item", "Order Date":"order_date", "Delivery Date":"delivery_date", "CustomerKey": "customer_id" , "StoreKey":"store_id" ,"ProductKey": "product_id","Quantity":"quantity", "Currency Code":"currency_code"})

# store
store = store.rename(columns={"StoreKey":"store_id", "State":"store_state", "Square Meters":"square_meters", "Open Date":"open_date"})


# ----------------------INFORMATION SUR LES TYPES DE DONNEES------------------------------

#print(customer.info())#
#print(data.info())
#print(exchange.info())
#print(product.info())
#print(sales.info())
#print(store.info())

# ----------------------MODIFICATION DES TYPES DE DONNEES NECESSAIRES------------------------------



# customer
customer['customer_id'] = customer['customer_id'].astype(str)
customer['cst_birthday'] = pd.to_datetime(customer['cst_birthday'], format='%m/%d/%Y')

#print(customer.info())


# exchange
exchange['exchange_date'] = pd.to_datetime(exchange['exchange_date'], format='%m/%d/%Y')

#!!!!A FAIRE: transformer les "." en "," sans convertir le type de données dans la colonne exchange
# print(exchange.info())


# product
product['product_id'] = product['product_id'].astype(str)
product['unit_cost_USD'] = product['unit_cost_USD'].str.replace('$', '', regex=False)
product['unit_cost_USD'] = product['unit_cost_USD'].str.replace(',', '', regex=False)
product['unit_cost_USD'] = product['unit_cost_USD'].str.replace('.', ',', regex=False)
product['unit_cost_USD'] = product['unit_cost_USD'].str.replace(',', '.', regex=False).astype(float)
product['unit_price_USD'] = product['unit_price_USD'].str.replace('$', '', regex=False)
product['unit_price_USD'] = product['unit_price_USD'].str.replace(',', '', regex=False)
product['unit_price_USD'] = product['unit_price_USD'].str.replace('.', ',', regex=False)
product['unit_price_USD'] = product['unit_price_USD'].str.replace(',', '.', regex=False).astype(float)
product['subcategory_id'] = product['subcategory_id'].astype(str)
product['category_id'] = product['category_id'].astype(str)

#print(product.info())


# sales

sales['order_number'] = sales['order_number'].astype(str)
sales['order_date'] = pd.to_datetime(sales['order_date'], format='%m/%d/%Y')
sales['delivery_date'] = pd.to_datetime(sales['delivery_date'], format='%m/%d/%Y')
sales['customer_id'] = sales['customer_id'].astype(str)
sales['store_id'] = sales['store_id'].astype(str)
sales['product_id'] = sales['product_id'].astype(str)

#print(sales.info())


# store
store['store_id'] = store['store_id'].astype(str)
#!!!!A FAIRE: transformer les "." en "," sans convertir le type de données dans la colonne square_meters
store['open_date'] = pd.to_datetime(store['open_date'], format='%m/%d/%Y')

#print(store.info())


# ----------------------JOINTURE DES DATASETS------------------------------

df_1 = pd.merge(sales, customer, how= "inner", on='customer_id')

df_2 = pd.merge(df_1, store,how= "inner", on='store_id')

df = pd.merge(df_2, product,how= "inner", on='product_id')

print(df.info())