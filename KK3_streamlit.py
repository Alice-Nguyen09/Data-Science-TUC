
import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

tab1, tab2, tab3 = st.tabs(["🏠 Hem", "🚗 Bilförsäljning", "📊 Dataanalys"])

with tab1:
    st.title("🏠 Hem")
    st.write("TACK FÖR ATT NI ÄR HÄR IDAGGGGG.")
    st.image('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/tack_730.jpg')


with tab2:
    st.title("🚗 Bilförsäljning")
    st.write("Här visas bilförsäljningar i England och United State.")



with tab3:
    st.title("📊 Dataanalys")
    st.write("Här visas dataanalyser och grafer.")
    st.subheader ('1. Vilka är 5 bilmärke har det högsta genomsnittliga försäljningspriset i respektiv land?')
    
    conn = sqlite3.connect('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/bilförsäljning_kunskapskontroll_3.csv.db')
    
    query = '''
    WITH RankedMakes AS (
    SELECT Country, Make, AVG(Pricesold) AS AvgPrice,
           ROW_NUMBER() OVER (PARTITION BY Country ORDER BY AVG(Pricesold_dollar) DESC) AS Rank
    FROM bilförsäljning_kunskapskontroll_3
    GROUP BY Country, Make)
    SELECT Country, Make, AvgPrice
    FROM RankedMakes
    WHERE Rank <= 5
    ORDER BY Country, Rank;
    '''

    result = pd.read_sql_query(query, conn)
    st.dataframe(result)


    st.subheader ('5 bilmärke med högsta försäljningspris')
    st.bar_chart(
    result, 
    x="Make", 
    y="AvgPrice", 
    color="Country", 
    stack=False,)


    st.subheader('2. Flest bilar sålt')
    st.text('Landet som säljer flest bilar av Mercedes-Benz (Make) och SUV (Bodytype) och Rear (Drivetype)?')

    conn = sqlite3.connect('/Users/AliceNguyen/Documents/Data Manager - TUC/(År 1.4) Data Science/bilförsäljning_kunskapskontroll_3.csv.db')

    query = '''
    SELECT Country, COUNT(*) AS TotalSales
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Make = 'Mercedes-Benz' AND Bodytype = 'Sedan' AND Drivetype = 'Rear'
    GROUP BY Country
    ORDER BY TotalSales DESC;
    '''

    result_Mercedes = pd.read_sql_query(query, conn)
    st.dataframe(result_Mercedes)

    st.text('Landet säljer flest bilar av Porsche (Make) och SUV (Bodytype) och Full (Drivetype)?')

    query = '''
    SELECT Country, COUNT(*) AS TotalSales
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Make = 'Porsche' AND Bodytype = 'Sedan' AND Drivetype = 'Full'
    GROUP BY Country
    ORDER BY TotalSales DESC;
    '''

    result_Porsche = pd.read_sql_query(query, conn)
    st.dataframe(result_Porsche)



    st.subheader('3. Bodytype som är mest populära (procentenhet).')
    st.text ('De 5 populära bodytyp i England.')

    query = '''
    SELECT 
    Country, 
    Bodytype, 
    COUNT(*) AS TotalSales, 
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY Country), 2) AS Percentage
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Country = 'England'
    GROUP BY Country, Bodytype
    ORDER BY Country, TotalSales DESC
    LIMIT 5;
    '''

    result_England = pd.read_sql_query(query, conn)
    st.dataframe (result_England)

    st.text('De 5 mest populära bodytyp i United State.')
    query = '''
    SELECT 
        Country, 
        Bodytype, 
        COUNT(*) AS TotalSales, 
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY Country), 2) AS Percentage
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Country = 'United State'
    GROUP BY Country, Bodytype
    ORDER BY Country, TotalSales DESC
    LIMIT 5;

    '''
    result_USA = pd.read_sql_query(query, conn)

    st.dataframe(result_USA)


    st.subheader ('4. Vilka bilmärke kan säljas för högre än 100000 för mileage högre än 1000?')

    query = '''
    SELECT 
        Country, 
        Make,
        Model,
        Mileage,
        Pricesold_dollar, 
        COUNT(*) AS TotalSales
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Pricesold_dollar > 10000 AND Mileage > 1000
    GROUP BY Country, Make, Model, Mileage, Pricesold_dollar
    HAVING COUNT(*) > 2
    ORDER BY Country, Pricesold_dollar DESC, TotalSales DESC;
    '''

    df = pd.read_sql_query(query, conn)
    st.dataframe(df)


    st.subheader ('5.Vilka bilar håller värdet bäst respektiv land?')

    query = '''
    SELECT 
        Country, 
        Make, 
        Model, 
        AVG(Pricesold_dollar / Mileage) AS PricePerMile
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Country = 'England'
    GROUP BY Country, Make, Model
    ORDER BY Country, PricePerMile DESC
    LIMIT 10;
    '''
    df1 = pd.read_sql(query, conn)

    query = '''
    SELECT 
        Country, 
        Make, 
        Model, 
        AVG(Pricesold_dollar / Mileage) AS PricePerMile
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Country = 'United State'
    GROUP BY Country, Make, Model
    ORDER BY Country, PricePerMile DESC
    LIMIT 10;
    '''
    df2 = pd.read_sql(query, conn)

    Bilar_håller_bäst_värde = pd.concat([df1, df2], ignore_index=True)
    st.dataframe(Bilar_håller_bäst_värde)


    st.subheader("6. Är Full-bilar dyrare än Front och Rear?")

    query = '''
    SELECT 
    Country, Drivetype, AVG(Pricesold_dollar) AS AveragePrice
    FROM bilförsäljning_kunskapskontroll_3
    WHERE Drivetype IN ('Full', 'Rear', 'Front')
    GROUP BY Country, Drivetype
    ORDER BY Country, AveragePrice DESC;
    '''
    df = pd.read_sql(query, conn)
    st.dataframe (df)

    import matplotlib.pyplot as plt
    import seaborn as sns

    conn.close()

    # Kontrollera om df har data
    if df.empty:
        st.warning("Inga data hittades för vald filtrering.")
    else:
        # Ställ in färgtema för Seaborn
        sns.set_style("whitegrid")

        # Skapa Matplotlib-figuren
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x="Country", y="AveragePrice", hue="Drivetype", ax=ax)

        # Diagram-titlar och etiketter
        ax.set_title("Jämförelse av genomsnittligt pris för 4WD, FWD och RWD i England och USA", fontsize=14)
        ax.set_xlabel("Land", fontsize=12)
        ax.set_ylabel("Genomsnittligt pris ($)", fontsize=12)
        ax.legend(title="Drivtyp")

        # Visa diagrammet i Streamlit
        st.pyplot(fig)