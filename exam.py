import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
from streamlit_option_menu import option_menu
import plotly.express as px
from cleaner import clean



st.set_page_config(
    page_title="Accademic Success",
    page_icon=":dart:",
    layout="wide",
    initial_sidebar_state="expanded")


df = pd.read_csv("17.csv")

with st.sidebar:
    selected = option_menu(
        menu_title='Menyular paneli',
        options=['Bosh Sahifa', 'Jadval Haqida', 'Loyiha'],
        orientation='vertical',
        icons=['house', 'info', 'bar-chart']
    )
    if selected == "Jadval Haqida":
        clean(df)
        option = st.multiselect(
        "Qanday yoqilgi turidagi avtomobillarning malumotini ko'rmoqchisiz",
        df["fuel"].unique(),
        df['fuel'].unique()[2])
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())
        selected_year = st.slider('Yilini tanlang:', min_year, max_year, (min_year, max_year))
        years= []
        for i in range(selected_year[0], selected_year[-1], 1):
            years.append(i)
   
# Bosh sahifa

if selected == "Bosh Sahifa":
    st.write("## DataFrame haqida ")
    st.write("### Ushbu datafreamda Avtomobilllar haqidagi malumotlarini ko'rishingiz mumkin")
    with st.expander("See dataframe"):
        st.write("## DataFrame")
        st.write(df)
    st.write("## DataFrame ning holati")
    st.write(df.describe())
        # Ikkita ustun:
    col1, col2 = st.columns(2)
    # Data Type lar
    with col1:
        st.subheader("Data Types:")
        st.table({"DataTypes": df.dtypes})
     
    # Column nomlari
    with col2:
        st.subheader("Columns:")
        st.table({"Nunique":df.nunique()})


# Jadval haqida

if selected == "Jadval Haqida":
    st.write("## DataFrame haqida ")
    with st.expander("See dataframe"):
        st.write("## DataFrame")
        st.write(df)
    st.write("## DataFrame ning holati")
    st.write(df.describe())
       
    col1, col2 = st.columns(2)
    # Data Type lar
    with col1:
        st.subheader("Nan counts:")
        st.table({"Nan counts": df.isna().sum()})
     
    # Column nomlari
    with col2:
        st.subheader("Nan  percentn %:")
        st.table({"Nan Percent":df.isna().mean()*100 })
    st.write(" ### Numeric tipidagi Nanlarni nima qilmoqchisiz")
    if st.button("Fillna"):
        clean(df)
    with st.expander("Nanlarni korish"):
        st.subheader("Nan counts:")
        st.table({"Nan counts": df.isna().sum()})

    df_selection = df.query('fuel in @option & year in @years')
    st.dataframe(df_selection)
    left, right= st.columns(2)
    with left:
        st.write(f"#### Avtomobillarning o'rtacha narxi\n ### {round(df_selection['selling_price'].mean())} $")
    with right:
        st.write(f"#### Avtomobillarnig o'rtacha probegi\n\n\n ### {round(df_selection['km_driven'].mean())} km")


elif selected == "Loyiha":
    st.write("## DataFrame haqida ")
    with st.expander("See dataframe"):
        st.write("## DataFrame")
        st.write(clean(df))
    # def loyiha():
    st.subheader(':bar_chart: Avtomobillar tahlili')
    import plotly.express as px

# Assuming df is your DataFrame

    left, middle, right = st.columns(3)

    with left:
    
        fuel_counts = df['fuel'].value_counts()
        fig = px.pie(
            values=fuel_counts.values, 
            names=fuel_counts.index, 
            title='Yoqilgi Turi',
            hole=0.6)
        st.plotly_chart(fig)

    with middle:
        
        transmission_counts = df['transmission'].value_counts()
        fig = px.pie(
            values=transmission_counts.values, 
            names=transmission_counts.index, 
            title='Uzatmalar qutisi',
            hole=0.6
        )
        st.plotly_chart(fig)

    with right:
        
        owner_counts = df['owner'].value_counts()
        fig = px.pie(
            values=owner_counts.values, 
            names=owner_counts.index, 
            title='Mashina egasi',
            hole=0.6
        )
        st.plotly_chart(fig)
    
    st.title("Munosabatlarni ko'rsatish: Turli ustunlar va Savdo narxi")
    cols = ['year', 'fuel', 'seller_type', 'transmission', 'owner', 'seats']
    select_option = st.selectbox("## Narx bilan nimalarni ko'rmoqchiasiz", (cols))

    for c in cols:
        if select_option ==c:
            fig, ax = plt.subplots(figsize=(10, 6))
            df.groupby(c)['selling_price'].mean().plot(kind='bar', ax=ax)
            ax.set_xlabel(c)
            ax.set_ylabel('Selling Price')
            ax.set_title(f'{c} vs Selling Price')
            st.pyplot(fig)


    option = st.selectbox("Nimalarni ko'rmoqchiasiz",
                          (df["transmission"].unique()))
   
   
    if option == "Manual":
        df_selection = df.query('transmission in @option ')
        st.dataframe(df_selection)
    
    st.header("Heat Map")
    left, right = st.columns(2)

    
    

    transmission = st.selectbox(
        "Janrlarni Filtrlash Hususiyati",
        options=df['transmission'].unique(),
        )



    if transmission == 'Automatic':
        df_selection = df.query('transmission in @option ')
        st.title('Heatmap in Streamlit')
        df_selection["max_power"]=pd.to_numeric(df_selection["max_power"], errors="coerce") 
        corr = df_selection[['selling_price','engine',  'max_power', 'km_driven']].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
        ax.set_title('Heatmap of Correlation Matrix')
        st.write("### Heatmap")
        st.pyplot(fig)


    if transmission == 'Manual':
        df_selection = df.query('transmission in @option ')
        st.title('Heatmap in Streamlit')
        df_selection["max_power"]=pd.to_numeric(df_selection["max_power"], errors="coerce") 
        corr = df_selection[['selling_price','engine',  'max_power', 'km_driven']].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
        ax.set_title('Heatmap of Correlation Matrix')
        st.write("### Heatmap")
        st.pyplot(fig)
