
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

   # Configurer l'affichage de la page Streamlit
st.set_page_config(page_title="Analyse des Données Commerciales", layout="wide")

   # Charger les données
@st.cache
def load_data():
       cst_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Customers.csv"
       prod_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Products.csv"
       sls_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Sales.csv"
       str_path= "C:/Users/SALIF/Desktop/projet_1/datasets/Stores.csv"

       customers = pd.read_csv(cst_path, encoding='ISO-8859-1')
       products = pd.read_csv(prod_path, encoding='ISO-8859-1')
       sales = pd.read_csv(sls_path, encoding='ISO-8859-1')
       stores = pd.read_csv(str_path, encoding='ISO-8859-1')

       return customers, products, sales, stores

   # Traitement des données
def preprocess_data(customers, products, sales, stores):
       customers = customers.rename(columns={
           "CustomerKey": "customer_id", "Gender": "gender", "Name": "name", "State Code": "cst_state_code",
           "State": "cst_state", "Zip Code": "cst_zip_code", "Continent": "continent", "Birthday": "birthday",
           "City":"cst_city", "Country":"cst_country"
       })
       
       products = products.rename(columns={
           "ProductKey": "product_id", "Product Name": "Product_name", "Brand": "brand", "Color": "color",
           "Unit Cost USD": "unit_cost_USD", "Unit Price USD": "unit_price_USD", "SubcategoryKey": "subcategory_id",
           "Subcategory": "subcategory", "CategoryKey": "Category_id", "Category":"category"
       })
       
       sales = sales.rename(columns={
           "Order Number": "order_id", "Line Item": "line_itm", "Order Date": "order_Date", "Delivery Date": "delivery_date",
           "CustomerKey":"customer_id", "StoreKey": "store_id","ProductKey": "product_id", "Quantity" : "qtity",
           "Currency Code" : "currency_id"
       })
       
       stores = stores.rename(columns={
           "StoreKey":"store_id", "Country": "st_country", "State" : "st_state",
           "Square Meters": "square_meters","Open Date":"open_date"
       })
       
       # Conversion des dates et des données numériques
       sales['order_Date'] = pd.to_datetime(sales['order_Date'], format='%m/%d/%Y')
       sales['delivery_date'] = pd.to_datetime(sales['delivery_date'], format='%m/%d/%Y')
       sales['DeliveryDelay'] = sales['delivery_date'].fillna(pd.to_datetime('NaT')) - sales['order_Date']
       sales['DeliveryDelay'] = sales['DeliveryDelay'].dt.days.fillna(-1)

       mean_delivery_delay = sales[sales['DeliveryDelay'] > -1]['DeliveryDelay'].mean()
       sales['delivery_date'] = sales.apply(
           lambda row: row['order_Date'] + pd.Timedelta(days=mean_delivery_delay) if row['DeliveryDelay'] == -1 else row['delivery_date'],
           axis=1
       )

       # Fusion des tables
       df_1 = pd.merge(sales, customers, how="inner", on='customer_id')
       df_2 = pd.merge(df_1, stores, how="inner", on='store_id')
       df = pd.merge(df_2, products, how="inner", on='product_id')

       # Conversion des colonnes numériques
       df['unit_cost_USD'] = df['unit_cost_USD'].str.replace('$', '').str.replace(',', '').str.replace('.', ',', regex=False).str.replace(',', '.').astype(float)
       df['unit_price_USD'] = df['unit_price_USD'].str.replace('$', '').str.replace(',', '').str.replace('.', ',', regex=False).str.replace(',', '.').astype(float)

       # Ajouter des colonnes utiles
       df['Revenue'] = df['qtity'] * df['unit_price_USD']
       df['Month'] = df['order_Date'].dt.to_period('M')

       return df

   # Charger et pré-traiter les données
customers, products, sales, stores = load_data()
df = preprocess_data(customers, products, sales, stores)

   # 1. Comprendre le Comportement des Clients

st.title("Analyse des Données Commerciales")

st.header("1. Comprendre le Comportement des Clients")

   # Tendances d'Achat
st.subheader("Tendances d'Achat")
monthly_orders = df.groupby('Month')['order_id'].count()
st.line_chart(monthly_orders)
st.markdown("Interprétation: Ce graphique montre comment les ventes évoluent au fil du temps. Une tendance croissante indique un marché en expansion, tandis qu'une tendance à la baisse pourrait suggérer des problèmes.")

   # Segmentation de la Clientèle
st.subheader("Segmentation de la Clientèle")
top_customers = df.groupby('customer_id')['Revenue'].sum().nlargest(20)
st.bar_chart(top_customers)
st.markdown("Interprétation: Le diagramme de Pareto peut révéler que 20% des clients génèrent 80% des ventes. Cela peut aider l'entreprise à cibler ses efforts marketing sur les segments de clientèle les plus profitables.")

   # Satisfaction Client (exemple hypothétique, remplacer par les vraies données si disponibles)
st.subheader("Satisfaction Client")
   # Supposons que la satisfaction client soit liée à la catégorie de produit (exemple hypothétique)
category_satisfaction = df.groupby('category')['Revenue'].sum()
st.bar_chart(category_satisfaction)
st.markdown("Interprétation: Les graphiques en barres pour les scores de satisfaction permettent d’identifier les produits ou services qui plaisent le plus ou le moins aux clients.")

   # 2. Optimiser les Performances des Produits

st.header("2. Optimiser les Performances des Produits")

   # Produits les Plus Populaires
st.subheader("Produits les Plus Populaires")
top_products = df.groupby('Product_name')['qtity'].sum().nlargest(10)
st.bar_chart(top_products)
st.markdown("Interprétation: Ce graphique montre quels produits se vendent le mieux.")

   # Marges Bénéficiaires
st.subheader("Marges Bénéficiaires")
product_margins = df.groupby('Product_name').apply(lambda x: (x['unit_price_USD'] - x['unit_cost_USD']).sum()).nlargest(10)
st.bar_chart(product_margins)
st.markdown("Interprétation: Ce graphique permet de voir quels produits génèrent les marges les plus élevées.")

   # 3. Évaluer l'Efficacité des Campagnes Marketing

st.header("3. Évaluer l'Efficacité des Campagnes Marketing")

   # Impact des Campagnes sur les Ventes (exemple hypothétique, remplacer par les vraies données si disponibles)
st.subheader("Impact des Campagnes sur les Ventes")
   # Supposons que les campagnes marketing ont été menées pendant certains mois
campaign_sales = df.groupby('Month')['Revenue'].sum()
st.line_chart(campaign_sales)
st.markdown("Interprétation: Ce graphique permet de voir l'impact direct des campagnes marketing sur les ventes.")

   # 4. Analyser les Tendances du Marché

st.header("4. Analyser les Tendances du Marché")

   # Tendances Saisonnières
st.subheader("Tendances Saisonnières")
seasonal_trends = df.groupby(df['order_Date'].dt.month)['Revenue'].sum()
st.line_chart(seasonal_trends)
st.markdown("Interprétation: Ce graphique montre les variations saisonnières des ventes.")
   # Variations des Prix
st.subheader("Variations des Prix")
price_variations = df.groupby('Month')['unit_price_USD'].mean()
st.line_chart(price_variations)
st.markdown("Interprétation: En suivant les variations de prix, l’entreprise peut comprendre comment les fluctuations de prix affectent les ventes.")

if st.button('Refresh Data'):
       st.experimental_rerun()
   

