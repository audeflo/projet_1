
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import os


# Configurer l'affichage de la page Streamlit
st.set_page_config(page_title="Analyse des Données e-sunu shop 🛒", page_icon="🛒", layout="wide")
logo_path = "./images/logo.jpg"
st.image(logo_path, width=200)
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
st.title("TABLEAU DE BORD DE e-sunu shop")
st.markdown('''
    <style>
    div.block-container{padding-top:1rem;}
    font-family: 'Roboto', sans-serif;
    color: blue;
    </style>
    ''', unsafe_allow_html=True)

# ----------------------IMPORTATION DES DONNEES------------------------------
@st.cache #_data
def importation(path):
    return pd.read_csv(path, encoding='ISO-8859-1')

# Chargement des données


# customers
print("TABLE CUSTOMERS")
cst_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Customers.csv"
customer = importation(cst_path)

#customer.head()

# exchange
print("TABLE EXCHANGE")
exc_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Exchange_Rates.csv"
exchange = importation(exc_path)
#exchange.head()


# product
print("TABLE PRODUCT")
prod_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Products.csv"
product = importation(prod_path)
#product.head()


# sales
print("TABLE SALES")
sls_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Sales.csv"
sales = importation(sls_path)
#sales.head()


# store
print("TABLE STORE")
str_path = "C:/Users/SALIF/Desktop/projet_1/datasets/Stores.csv"
store = importation(str_path)
#store.head()

# ----------------------RENOMMER LES COLONNES------------------------------
# ----------------------RENOMMER LES COLONNES------------------------------


#customer
customer= customer.rename(columns={"CustomerKey": "customer_id","Gender": "gender", "Name": "name", "City":"cst_city","State Code": "cst_state_code","State" : "cst_state","Zip Code":"cst_zip_code","Country" : "cst_country","Continent": "cst_continent","Birthday":"cst_birthday"})
#customer.info()

# exchange
exchange = exchange.rename(columns={"Date": "exchange_date", "Currency":"currency_code", "Exchange":"exchange"})
#exchange.info()


# product
product = product.rename(columns={"ProductKey": "product_id","Product Name": "product_name",
"Brand": "brand", "Color": "color", "Unit Cost USD": "unit_cost_USD","Unit Price USD": "unit_price_USD", 
"SubcategoryKey": "subcategory_id","Subcategory": "subcategory", "CategoryKey": "category_id", "Category":"category"})

#product.info()

# sales
sales = sales.rename(columns={"Order Number" : "order_number","Line Item" : "line_item", "Order Date":"order_date",
"Delivery Date":"delivery_date", "CustomerKey": "customer_id" , "StoreKey":"store_id" ,"ProductKey": "product_id",
"Quantity":"quantity", "Currency Code":"currency_code"})
sales.info()

# store
store = store.rename(columns={"StoreKey":"store_id","State":"store_state", "Square Meters":"square_meters", "Open Date":"open_date", "Country":"st_country"})
#store.info()


# ----------------------MODIFICATION DES TYPES DE DONNEES NECESSAIRES------------------------------
# ----------------------MODIFICATION DES TYPES DE DONNEES NECESSAIRES------------------------------

# customer
customer['customer_id'] = customer['customer_id'].astype(str)

customer['cst_birthday'] = pd.to_datetime(customer['cst_birthday'], format='%m/%d/%Y')

#customer.info()
#customer.head()


# exchange
exchange['exchange_date']  = pd.to_datetime(exchange['exchange_date'] )
exchange['exchange_date']  = exchange['exchange_date'] .dt.strftime('%m/%d/%Y')

exchange['exchange'] = exchange['exchange'].astype(str).str.replace('.', ',')
exchange['exchange'] = exchange['exchange'].str.replace(',', '.').astype(float)

#exchange.info()
#exchange.head()


# product

product['product_id'] = product['product_id'].astype(str)

product['unit_cost_USD'] = product['unit_cost_USD'].astype(str).str.replace('$', '')
product['unit_cost_USD'] = product['unit_cost_USD'].astype(str).str.replace(',', '')
product['unit_cost_USD'] = product['unit_cost_USD'].astype(str).str.replace('.', ',')
product['unit_cost_USD'] = product['unit_cost_USD'].str.replace(',', '.').astype(float)

product['unit_price_USD'] = product['unit_price_USD'].astype(str).str.replace('$', '')
product['unit_price_USD'] = product['unit_price_USD'].astype(str).str.replace(',', '')
product['unit_price_USD'] = product['unit_price_USD'].astype(str).str.replace('.', ',')
product['unit_price_USD'] = product['unit_price_USD'].str.replace(',', '.').astype(float)

# enlever le nom des marques sur le nom du produit
product['product_name'] = product['product_name'].astype(str).str.replace('Contoso', '')
product['product_name'] = product['product_name'].astype(str).str.replace('WWI', '')
product['product_name'] = product['product_name'].astype(str).str.replace('NT', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Adventure Works', '')
product['product_name'] = product['product_name'].astype(str).str.replace('SV', '')
product['product_name'] = product['product_name'].astype(str).str.replace('A. Datum', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Fabrikam', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Litware ', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Proseware', '')
product['product_name'] = product['product_name'].astype(str).str.replace('MGS ', '')
product['product_name'] = product['product_name'].astype(str).str.replace('The Phone Company', '')

# enlever les couleurs dans le nom du produit
product['product_name'] = product['product_name'].astype(str).str.replace('Azure', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Black', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Blue', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Brown', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Grey', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Gold', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Green', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Orange', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Pink', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Purple', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Red', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Silver', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Silver Grey', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Transparent', '')
product['product_name'] = product['product_name'].astype(str).str.replace('White', '')
product['product_name'] = product['product_name'].astype(str).str.replace('Yellow', '')

product['subcategory_id'] = product['subcategory_id'].astype(str)

product['category_id'] = product['category_id'].astype(str)

#product.info()
#product.head()


# sales

sales['order_number'] = sales['order_number'].astype(str)

sales['order_date'] = pd.to_datetime(sales['order_date'])

sales['delivery_date'] = pd.to_datetime(sales['delivery_date'])

sales['customer_id'] = sales['customer_id'].astype(str)

sales['store_id'] = sales['store_id'].astype(str)

sales['product_id'] = sales['product_id'].astype(str)

#sales.info()
#sales.head()


# store
store['store_id'] = store['store_id'].astype(str)

store['square_meters'] = store['square_meters'].astype(str).str.replace('.', ',')
store['square_meters'] = store['square_meters'].str.replace(',', '.').astype(float)

store['open_date'] = pd.to_datetime(store['open_date'])

#store.info()
#store.head()

# ----------------------JOINTURE DES DATASETS------------------------------
df_1 = pd.merge(sales, customer, how= "inner", on='customer_id')

df_2 = pd.merge(df_1, store,how= "inner", on='store_id')

df = pd.merge(df_2, product,how= "inner", on='product_id')

#df.info()
#df.head()

df['order_year'] = df['order_date'].dt.year
df['Month'] = df['order_date'].dt.to_period('M')
df['Revenue'] = df['quantity'] * df['unit_price_USD']
# ----------------------CREATION DES GRAPHIQUES------------------------------
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
selected_color = st.sidebar.multiselect("Sélectionnez un ou plusieurs Pays", df['color'].unique())
selected_year = st.sidebar.multiselect("Sélectionnez un ou plusieurs Années", df['order_year'].unique())

filtered_df = df[
    (df['category'].isin(selected_category) if selected_category else df['category'].notnull()) &
    (df['Month'].astype(str).isin(selected_month) if selected_month else df['Month'].notnull()) &
    (df['color'].isin(selected_color) if selected_color else df['color'].notnull())&
    (df['order_year'].isin(selected_year) if selected_year else df['order_year'].notnull()) 
    

]

# GRAPHIQUE 1: VENTES TOTALES (CHIFFRE D'AFFAIRES)
sales['delivery_delay'] = sales['delivery_date'].fillna(pd.to_datetime('NaT')) - sales['order_date']
sales['delivery_delay'] = sales['delivery_delay'].dt.days.fillna(-1)  # Remplacer NaT par -1

mean_delivery_delay = sales[sales['delivery_delay'] > -1]['delivery_delay'].mean() 
sales['delivery_date'] = sales.apply(lambda row: row['order_date'] + pd.Timedelta(days=mean_delivery_delay) if row['delivery_delay'] == -1 else row['delivery_date'],
    axis=1)

print(f"Le temps de livraison moyen est de {mean_delivery_delay:.2f} jours.")
# Calcul des ventes totales pour chaque transaction
df['total_sales'] = df['quantity'] * df['unit_price_USD']

# Calcul du chiffre d'affaires total
total_revenue = df['total_sales'].sum()
qty_sold = float(filtered_df['quantity'].sum())
top_category = filtered_df['category'].mode().to_string(index=False)
top_store = filtered_df['st_country'].mode().to_string(index=False)
# Affichage des KPI
total1, total2, total3, total4, total5 = st.columns(5, gap="small")

with total1:
    st.info('Ventes totales', icon="📈")
    st.metric(label='', value=f"$ {total_revenue:,.0f}")

with total2:
    st.info('Qté vendue', icon="🛒")
    st.metric(label='', value=f"{qty_sold:,.0f}")

with total3:
    st.info('Catégorie supérieure', icon="🏢")
    st.metric(label='', value=top_category)

with total4:
    st.info('Top Store', icon="🏬")
    st.metric(label='', value=top_store)
    
with total5:
    st.info('Temps de livraison moyen', icon="🚚")
    st.metric(label='', value=mean_delivery_delay)

   
# 1. Comprendre le Comportement des Clients
#df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y')

st.header("1. Comprendre le Comportement des Clients")
st.subheader("Tendances d'Achat")
monthly_orders = filtered_df.groupby('Month')['order_number'].count()
st.line_chart(monthly_orders)   
# 2. Optimiser les Performances des Produits
st.header("2. Optimiser les Performances des Produits")


# Chiffre d'Affaires par Mois
st.title('Chiffre d\'Affaires par Mois')
st.subheader("Chiffre d'Affaires par Mois")
monthly_revenue = filtered_df.groupby('Month')['Revenue'].sum()
st.line_chart(monthly_revenue)
st.markdown("Interprétation: ")


# Chiffre d'Affaires par Produit
st.title('Produit avec le Plus de Ventes')
st.subheader("Top 10 des Produits par Chiffre d'Affaires")
top_products_revenue = filtered_df.groupby('product_name')['Revenue'].sum().nlargest(10)
st.bar_chart(top_products_revenue)
st.markdown("Interprétation: ")


# Mois avec le Plus de Ventes
st.title('Mois avec le Plus de Ventes')
st.subheader("Mois avec le Plus de Ventes")
best_month = monthly_revenue.idxmax()
st.write(f"Le mois avec le plus de ventes est {best_month} avec un chiffre d'affaires de {monthly_revenue.max():,.2f} USD.")


# Analyse des Catégories Sous-Représentées
st.title('Catégories Sous-Représentées')
st.subheader("Analyse des Catégories Sous-Représentées")
category_revenue = filtered_df.groupby('category')['Revenue'].sum()
min_category = category_revenue.idxmin()
min_category_revenue = category_revenue.min()
st.write(f"La catégorie avec le revenu le plus bas est '{min_category}' avec un chiffre d'affaires de ${min_category_revenue:,.2f}.")
st.markdown("Interprétation: ")

# Analyse de la Croissance par Pays
st.subheader("Analyse de la Croissance par Pays")
revenue_growth_by_country = filtered_df.groupby(['cst_country', 'Month'])['Revenue'].sum().unstack().pct_change(axis=1).mean(axis=1)
st.bar_chart(revenue_growth_by_country)
st.markdown("Interprétation: ")

# 5. Améliorer la Logistique et la Gestion des Stocks
st.header("5. Améliorer la Logistique et la Gestion des Stocks")

# Délai de Livraison Moyen
st.subheader("Délai de Livraison Moyen")
avg_delivery_delay = filtered_df.groupby('store_id')['delivery_date'].mean().sort_values()
st.bar_chart(avg_delivery_delay)
st.markdown("Interprétation: ")

# Quantités Vendues par Magasin
st.subheader("Quantités Vendues par Magasin")
qty_by_store = filtered_df.groupby('store_state')['quantity'].sum().sort_values(ascending=False)
st.bar_chart(qty_by_store)
st.markdown("Interprétation: ")


# GRAPHIQUE 3: histogramme de répartition des achats par tranche d'âge
st.title('Histogramme de répartition des achats par tranche d\'âge')
# Calculer l'âge en années
today = pd.to_datetime('today')
df['age'] = today.year - df['cst_birthday'].dt.year 
# Définir les tranches d'âge
bins = [0, 18, 25, 35, 45, 55, 65, 100]
labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
# Agréger les quantités d'achats par tranche d'âge
age_distribution = df.groupby('age_group', observed=False)['total_sales'].sum().reset_index()
# Tracer l'histogramme avec Streamlit
st.title('Répartition du chiffre d\'affaires par tranche d\'âge')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=age_distribution, x='age_group', y='total_sales', palette='viridis', ax=ax)
ax.set_title('Répartition du chiffre d\'affaires par tranche d\'âge')
ax.set_xlabel('Tranche d\'âge')
ax.set_ylabel('Quantité d\'achats')
st.pyplot(fig)
#Titre de l'application
st.title('Histogramme de répartition des achats par tranche d\'âge')




st.title('Quantité d\'achats par catégorie')
# Assurez-vous que les dates sont bien formatées
df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')
# Extraire l'année
df['delivery_year'] = df['delivery_date'].dt.year
# Agréger les ventes totales par marque et par année
annual_brand_sales = df.groupby(['delivery_year', 'brand'])['total_sales'].sum().reset_index()
# Créer le graphique à barres empilées horizontal avec plotly
fig = px.bar(
    annual_brand_sales,
    x='total_sales',
    y='delivery_year',
    color='brand',
    orientation='h',
    title='Part de chaque marque dans le chiffre d\'affaires par année',
    labels={'total_sales': 'Chiffre d\'affaires (USD)', 'delivery_year': 'Année'},
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=600
)
# Personnaliser la légende en haut
fig.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1,
        xanchor='right',
        x=1
    ),
    xaxis_title='Chiffre d\'affaires (USD)',
    yaxis_title='Année',
    barmode='stack',
    title={
        'text': "",#Part de chaque marque dans le chiffre d'affaire par année",
        'x': 0.5, # Position horizontale du titre (0= gauche, 0.5=centre, 1=droite)
        'y': 0.95, # Position verticale du titre
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=20, color='black', family='Arial')
    },
)
# Afficher le graphique avec Streamlit
#st.title('Part de chaque marque dans le chiffre d\'affaires par année')
st.plotly_chart(fig)

# # Agréger les ventes totales par année
# annual_sales = df.groupby('order_year')['total_sales'].sum().reset_index()
# # Définir l'index sur les années
# annual_sales.set_index('order_year', inplace=True)
# # Préparer les données pour la régression linéaire
# X = np.array(annual_sales.index).reshape(-1, 1)
# y = annual_sales['total_sales'].values
# # Ajouter une colonne de biais (intercept) à X
# X_b = np.c_[np.ones((X.shape[0], 1)), X]
# # Calculer les coefficients de la régression linéaire
# theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
# # Prévisions
# forecast_periods = 5
# forecast_years = np.array(range(annual_sales.index.max() + 1, annual_sales.index.max() + 1 + forecast_periods)).reshape(-1, 1)
# forecast_years_b = np.c_[np.ones((forecast_years.shape[0], 1)), forecast_years]
# forecast = forecast_years_b.dot(theta_best)
# # Créer un DataFrame pour les prévisions
# forecast_df = pd.DataFrame({
#     'forecast': forecast
# }, index=forecast_years.flatten())
# # Afficher les résultats avec Streamlit
# st.title('Prévisions des ventes annuelles')
# st.line_chart(annual_sales['total_sales'], label='Ventes réelles')
# st.line_chart(forecast_df['forecast'], label='Prévisions')
# # Afficher les prévisions sous forme de tableau
# st.write(forecast_df)

# # Carte géographique affichant la répartition du chiffre d'affaires par pays
# st.header("Répartition du chiffre d'affaires par pays")
# df['sales_value'] = df['unit_price_USD'] * df['quantity']
# sales_by_country = df.groupby('cst_country')['sales_value'].sum().reset_index()

# fig_geo = px.choropleth(sales_by_country, locations='cst_country', locationmode='country names',
#                         color='sales_value', hover_name='cst_country',
#                         color_continuous_scale='Viridis', title="Chiffre d'affaires par pays")
# st.plotly_chart(fig_geo)

# Assurez-vous que les dates sont bien formatées
#df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# Extraire l'année
#df['order_year'] = df['order_date'].dt.year

st.title('Orders by Year')
# Agréger les ventes totales par année
annual_sales = df.groupby('order_year')['total_sales'].sum().reset_index()
# Définir l'index sur les années
annual_sales.set_index('order_year', inplace=True)
# Préparer les données pour la régression linéaire
X = np.array(annual_sales.index).reshape(-1, 1)
y = annual_sales['total_sales'].values
# Ajouter une colonne de biais (intercept) à X
X_b = np.c_[np.ones((X.shape[0], 1)), X]
# Calculer les coefficients de la régression linéaire
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
# Prévisions
forecast_periods = 5
forecast_years = np.array(range(annual_sales.index.max() + 1, annual_sales.index.max() + 1 + forecast_periods)).reshape(-1, 1)
forecast_years_b = np.c_[np.ones((forecast_years.shape[0], 1)), forecast_years]
forecast = forecast_years_b.dot(theta_best)
# Créer un DataFrame pour les prévisions
forecast_df = pd.DataFrame({
    'forecast': forecast
}, index=forecast_years.flatten())
# Afficher les résultats avec Streamlit
st.title('Prévisions des ventes annuelles')
# Tracer les ventes réelles
fig, ax = plt.subplots()
ax.plot(annual_sales.index, annual_sales['total_sales'], label='Ventes réelles', marker='o')
# Tracer les prévisions
ax.plot(forecast_df.index, forecast_df['forecast'], label='Prévisions', marker='o')
ax.set_xlabel('Année')
ax.set_ylabel('Chiffre d\'affaires (USD)')
ax.legend()
st.pyplot(fig)

# Afficher les prévisions sous forme de tableau
st.write(forecast_df)

st.title('Afficher les 10 produits les plus vendus')
# Calculer les 10 produits les plus vendus
top_products = df.groupby('product_name')['quantity'].sum().nlargest(10)
# Créer le graphique avec Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
top_products.plot(kind='barh', ax=ax)
ax.set_title('Top 10 des produits les plus vendus')
ax.set_xlabel('Quantité vendue')
ax.set_ylabel('Produit')
# Afficher le graphique avec Streamlit
st.title('Top 10 des produits les plus vendus')
st.pyplot(fig)



# Calculer les ventes par catégorie
st.title('Répartition des ventes par catégorie')
category_sales = df.groupby('category')['quantity'].sum()
# Créer le graphique avec Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
category_sales.plot(kind='bar', ax=ax)
ax.set_title('Répartition des ventes par catégorie')
ax.set_xlabel('Catégorie')
ax.set_ylabel('Quantité vendue')
# Afficher le graphique avec Streamlit
st.title('Répartition des ventes par catégorie')
st.pyplot(fig)



# Calculer le revenu mensuel
#df['Revenue'] = df['qtity'] * df['unit_price_USD']
monthly_revenue = df.groupby('Month')['Revenue'].sum()
# Créer le graphique avec Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
monthly_revenue.plot(kind='line', ax=ax)
ax.set_title('Revenu total par mois')
ax.set_xlabel('Mois')
ax.set_ylabel('Revenu en USD')
# Afficher le graphique avec Streamlit
st.title('Revenu total par mois')
st.pyplot(fig)


#Calculer les ventes par couleur
st.title('Couleurs des produits les plus vendus')
color_sales = df.groupby('color')['quantity'].sum()
# Créer le graphique avec Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
color_sales.plot(kind='bar', ax=ax)
ax.set_title('Couleurs des produits les plus vendus')
ax.set_xlabel('Couleur')
ax.set_ylabel('Quantité vendue')
# Afficher le graphique avec Streamlit
st.title('Couleurs des produits les plus vendus')
st.pyplot(fig)


# Extraire le jour de la semaine
df['DayOfWeek'] = df['order_date'].dt.day_name()
# Calculer le nombre de commandes par jour de la semaine
day_of_week_orders = df['DayOfWeek'].value_counts()
# Créer le graphique avec Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
day_of_week_orders.plot(kind='bar', ax=ax)
ax.set_title('Distribution des commandes par jour de la semaine')
ax.set_xlabel('Jour de la semaine')
ax.set_ylabel('Nombre de commandes')
# Afficher le graphique avec Streamlit
st.title('Distribution des commandes par jour de la semaine')
st.pyplot(fig)
# # Ventes par année avec prévision
# st.header("Ventes par année et prévisions")
# df['year'] = df['order_date'].dt.year
# sales_per_year = df.groupby('year')['sales_value'].sum().reset_index()

# fig_sales_year = px.line(sales_per_year, x='year', y='sales_value', markers=True, title="Ventes par année")
# # Ajout d'une prévision simple en utilisant une régression linéaire
# from sklearn.linear_model import LinearRegression
# import numpy as np

# # Modèle de régression
# X = sales_per_year['year'].values.reshape(-1, 1)
# y = sales_per_year['sales_value'].values
# model = LinearRegression().fit(X, y)
# sales_per_year['forecast'] = model.predict(X)

# fig_sales_year.add_trace(go.Scatter(x=sales_per_year['year'], y=sales_per_year['forecast'],
#                                     mode='lines', name='Prévision', line=dict(dash='dash')))

# st.plotly_chart(fig_sales_year)

# # Analyse des fluctuations du marché (via les taux de change)
# st.header("Analyse des fluctuations du marché")
# exchange['exchange'] = exchange['exchange'].str.replace(',', '.').astype(float)
# exchange_rate_avg = exchange.groupby('currency_code')['exchange'].mean().reset_index()

# fig_exchange = px.bar(exchange_rate_avg, x='currency_code', y='exchange', title="Taux de change moyen par devise",
#                       color='exchange', color_continuous_scale='Magma')

# st.plotly_chart(fig_exchange)


# Conclusion et Recommandations
st.header("Conclusion et Recommandations")