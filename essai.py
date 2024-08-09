#Voici une version mise à jour de votre code qui intègre les fonctionnalités mentionnées dans le premier script dans le deuxième :


import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurer l'affichage de la page Streamlit
st.set_page_config(page_title="Analyse des Données  🛒", page_icon="🛒", layout="wide")

# ---- MASQUER LE STYLE STREAMLIT ----
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Titre de la page
st.title("TABLEAU DE BORD DES VENTES DES SUPERMARCHÉS")
st.markdown('''
    <style>
    div.block-container{padding-top:1rem;}
    font-family: 'Roboto', sans-serif;
    color: blue;
    </style>
    ''', unsafe_allow_html=True)

# Charger les données
@st.cache #_data(ttl=600) # Ajustez le ttl (durée de vie) selon vos besoins
def load_data():
    cst_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Customers.csv"
    prod_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Products.csv"
    sls_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Sales.csv"
    str_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Stores.csv"

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
    #sales['order_Date'] = pd.to_datetime(sales['order_Date'], format='%m/%d/%Y')
    #sales['delivery_date'] = pd.to_datetime(sales['delivery_date'], format='%m/%d/%Y')
    sales['order_Date'] = pd.to_datetime(sales['order_Date'], format='%m/%d/%Y', errors='coerce')

    sales['delivery_date'] = pd.to_datetime(sales['delivery_date'], format='%m/%d/%Y', errors='coerce')
    sales['DeliveryDelay'] = sales['delivery_date'].fillna(pd.to_datetime('NaT')) - sales['order_Date']
    sales['DeliveryDelay'] = sales['DeliveryDelay'].dt.days.fillna(-1)

    mean_delivery_delay = sales[sales['DeliveryDelay'] > -1]['DeliveryDelay'].mean()
    sales['delivery_date'] = sales.apply(
        lambda row: row['order_Date'] + pd.Timedelta(days=mean_delivery_delay) if row['DeliveryDelay'] == -1 else row['delivery_date'],
        axis=1
    )
    #sales['delivery_date'] = sales['delivery_date'].dt.date
    sales['order_Date'] = pd.to_datetime(sales['order_Date'], format='%Y/%m/%d', errors='coerce')

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

# Interface Streamlit
st.title("Tableau de Bord d'Analyse des Données Commerciales")
st.markdown("""
Ce tableau de bord vous permet d'explorer les données commerciales à travers divers graphiques interactifs.
Utilisez les filtres et les graphiques pour obtenir des insights précieux sur le comportement des clients, les performances des produits, et l'efficacité des campagnes marketing.
""")

# Sidebar pour les filtres
st.sidebar.header("Filtres")
selected_category = st.sidebar.multiselect("Sélectionnez une ou plusieurs Catégories", df['category'].unique())
selected_month = st.sidebar.multiselect("Sélectionnez un ou plusieurs Mois", df['Month'].astype(str).unique())
selected_country = st.sidebar.multiselect("Sélectionnez un ou plusieurs Pays", df['cst_country'].unique())

#filtered_df = df[
#    (df['category'].isin(selected_category) if selected_category else True) &
#    (df['Month'].astype(str).isin(selected_month) if selected_month else True) &
#    (df['cst_country'].isin(selected_country) if selected_country else True)
#]
filtered_df = df[
    (df['category'].isin(selected_category) if selected_category else df['category'].notnull()) &
    (df['Month'].astype(str).isin(selected_month) if selected_month else df['Month'].notnull()) &
    (df['cst_country'].isin(selected_country) if selected_country else df['cst_country'].notnull())
]

# Calculer les meilleures analyses
total_sales = float(filtered_df['Revenue'].sum())
qty_sold = float(filtered_df['qtity'].sum())
top_category = filtered_df['category'].mode().to_string(index=False)
top_store = filtered_df['st_country'].mode().to_string(index=False)

# Affichage des KPI
total1, total2, total3, total4 = st.columns(4, gap="small")

with total1:
    st.info('Ventes totales', icon="📈")
    st.metric(label='', value=f"$ {total_sales:,.0f}")

with total2:
    st.info('Qté vendue', icon="🛒")
    st.metric(label='', value=f"{qty_sold:,.0f}")

with total3:
    st.info('Catégorie supérieure', icon="🏢")
    st.metric(label='', value=top_category)

with total4:
    st.info('Top Store', icon="🏬")
    st.metric(label='', value=top_store)

st.markdown("""---""")

# 1. Comprendre le Comportement des Clients
st.header("1. Comprendre le Comportement des Clients")
st.write(df[['Month']].head())
# Tendances d'Achat
st.subheader("Tendances d'Achat")
monthly_orders = filtered_df.groupby('Month')['order_id'].count()
st.line_chart(monthly_orders)
st.markdown("Interprétation: Ce graphique montre comment les ventes évoluent au fil du temps.")

# Nombre de Clients
st.subheader("Nombre de Clients par Mois")
monthly_customers = filtered_df.groupby('Month')['customer_id'].nunique()
st.bar_chart(monthly_customers)
st.markdown("Interprétation: Le nombre de clients montre la portée de notre base de clientèle au fil du temps.")

# 2. Optimiser les Performances des Produits
st.header("2. Optimiser les Performances des Produits")

# Chiffre d'Affaires par Mois
st.subheader("Chiffre d'Affaires par Mois")
monthly_revenue = filtered_df.groupby('Month')['Revenue'].sum()
st.line_chart(monthly_revenue)
st.markdown("Interprétation: Ce graphique montre le chiffre d'affaires mensuel.")

# Chiffre d'Affaires par Produit
st.subheader("Top 10 des Produits par Chiffre d'Affaires")
top_products_revenue = filtered_df.groupby('Product_name')['Revenue'].sum().nlargest(10)
st.bar_chart(top_products_revenue)
st.markdown("Interprétation: Ce graphique montre les produits qui génèrent le plus de revenus.")

# Mois avec le Plus de Ventes
st.subheader("Mois avec le Plus de Ventes")
best_month = monthly_revenue.idxmax()
st.write(f"Le mois avec le plus de ventes est {best_month} avec un chiffre d'affaires de {monthly_revenue.max():,.2f} USD.")


# 3. Évaluer l'Efficacité des Campagnes Marketing 
st.header("3. Évaluer l'Efficacité des Campagnes Marketing")

# Répartition des Ventes par Pays
st.subheader("Répartition des Ventes par Pays")
sales_by_country = filtered_df.groupby('cst_country')['Revenue'].sum().sort_values(ascending=False)
st.bar_chart(sales_by_country)
st.markdown("Interprétation: Ce graphique montre comment les ventes sont réparties par pays, ce qui peut indiquer l'efficacité des campagnes marketing régionales.")

# Impact des Promotions sur les Ventes
st.subheader("Impact des Promotions sur les Ventes")
promoted_sales = filtered_df[filtered_df['brand'] == 'Promoted'] # Filtre fictif pour les produits promus
non_promoted_sales = filtered_df[filtered_df['brand'] != 'Promoted']

promoted_revenue = promoted_sales['Revenue'].sum()
non_promoted_revenue = non_promoted_sales['Revenue'].sum()

st.write(f"Revenu des produits promus: ${promoted_revenue:,.2f}")
st.write(f"Revenu des produits non promus: ${non_promoted_revenue:,.2f}")
st.markdown("Interprétation: Cela montre l'impact des promotions sur le chiffre d'affaires.")

# 4. Identifier les Opportunités de Croissance
st.header("4. Identifier les Opportunités de Croissance")

# Analyse des Catégories Sous-Représentées
st.subheader("Analyse des Catégories Sous-Représentées")
category_revenue = filtered_df.groupby('category')['Revenue'].sum()
min_category = category_revenue.idxmin()
min_category_revenue = category_revenue.min()

st.write(f"La catégorie avec le revenu le plus bas est '{min_category}' avec un chiffre d'affaires de ${min_category_revenue:,.2f}.")
st.markdown("Interprétation: Cette information peut aider à identifier les catégories qui pourraient nécessiter des efforts supplémentaires pour augmenter leurs ventes.")

# Analyse de la Croissance par Pays
st.subheader("Analyse de la Croissance par Pays")
revenue_growth_by_country = filtered_df.groupby(['cst_country', 'Month'])['Revenue'].sum().unstack().pct_change(axis=1).mean(axis=1)
st.bar_chart(revenue_growth_by_country)
st.markdown("Interprétation: Ce graphique montre les taux de croissance des revenus par pays, ce qui peut indiquer où se trouvent les meilleures opportunités de croissance.")

# 5. Améliorer la Logistique et la Gestion des Stocks
st.header("5. Améliorer la Logistique et la Gestion des Stocks")

# Délai de Livraison Moyen
st.subheader("Délai de Livraison Moyen")
avg_delivery_delay = filtered_df.groupby('store_id')['DeliveryDelay'].mean().sort_values()
st.bar_chart(avg_delivery_delay)
st.markdown("Interprétation: Ce graphique montre le délai moyen de livraison par magasin, ce qui peut indiquer où des améliorations logistiques sont nécessaires.")

# Quantités Vendues par Magasin
st.subheader("Quantités Vendues par Magasin")
qty_by_store = filtered_df.groupby('st_state')['qtity'].sum().sort_values(ascending=False)
st.bar_chart(qty_by_store)
st.markdown("Interprétation: Ce graphique montre les quantités vendues par magasin, ce qui peut aider à optimiser la gestion des stocks.")

# Conclusion et Recommandations
st.header("Conclusion et Recommandations")

st.markdown("""
### Recommandations Principales :
1. **Concentrez les efforts marketing sur les pays à forte croissance** pour maximiser le retour sur investissement.
2. **Augmentez les promotions** pour les produits moins performants afin de stimuler les ventes.
3. **Améliorez les délais de livraison** dans les magasins avec des retards importants pour augmenter la satisfaction client.
4. **Optimisez la gestion des stocks** en tenant compte des ventes passées et des prévisions de demande.
""")


### Explications supplémentaires :
#- **Impact des Promotions sur les Ventes** : Ici, j'ai utilisé un filtre fictif (`brand == 'Promoted'`) pour simuler l'analyse des promotions. Vous devrez remplacer cela par un critère réel dans vos données.
#- **Analyse de la Croissance par Pays** : L'analyse de la croissance par pays est basée sur la variation moyenne du chiffre d'affaires par mois.
#- **Conclusion et Recommandations** : Enfin, j'ai ajouté une section de recommandations basée sur les insights précédents.

