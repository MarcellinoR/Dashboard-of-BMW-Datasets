import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sklearn.linear_model import LinearRegression

# 1. SETUP & STYLING
st.set_page_config(page_title="BMW Business Intelligence", layout="wide")

# CSS untuk membuat tampilan kotak (Cards) seperti di referensi
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0066bf;
    }
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABASE CONNECTION
engine = create_engine('mysql+pymysql://root:@localhost:3306/Car')

def fetch_data(query):
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

# 3. SIDEBAR & FILTERS
st.sidebar.image("https://www.bmw.com/etc.clientlibs/settings/wcm/designs/bmwcom/base/resources/ci2020/img/logo-bmw-menu.png", width=60)
st.sidebar.title("Control Panel")

list_model = fetch_data("SELECT DISTINCT model FROM bmw")['model'].tolist()
selected_model = st.sidebar.multiselect("Pilih Model:", list_model, default=list_model[:3])

# Filter dinamis berdasarkan multiselect
model_filter = f"('{  "','".join(selected_model)  }')" if selected_model else "('')"
df = fetch_data(f"SELECT * FROM bmw WHERE model IN {model_filter}")

# 4. HEADER & TOP METRICS
st.title("📊 BMW Sales Performance Dashboard")
st.markdown("---")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Inventory", f"{len(df):,}")
m2.metric("Avg Market Price", f"£{df['price'].mean():,.0f}")
m3.metric("Avg Mileage", f"{df['mileage'].mean():,.0f}")
m4.metric("Avg Engine Size", f"{df['engineSize'].mean():.1f}L")
m5.metric("Avg Efficiency", f"{df['mpg'].mean():.1f} MPG")

st.markdown("### Executive Overview")

# 5. MAIN VISUALIZATION (GRID LAYOUT)
row1_1, row1_2 = st.columns([2, 1])

with row1_1:
    st.subheader("Sales Trend & Price Evolution")
    # Menggabungkan Area Chart dan Line Chart
    df_trend = df.groupby('year')['price'].agg(['mean', 'count']).reset_index()
    fig_trend = px.area(df_trend, x='year', y='mean', title="Average Price Over Years",
                        line_shape='spline', color_discrete_sequence=['#0066bf'], template="plotly_dark")
    st.plotly_chart(fig_trend, use_container_width=True)

with row1_2:
    st.subheader("Transmission Mix")
    fig_donut = px.pie(df, names='transmission', hole=0.6, template="plotly_dark",
                       color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_donut, use_container_width=True)

row2_1, row2_2, row2_3 = st.columns(3)

with row2_1:
    st.subheader("Fuel Type Distribution")
    fig_fuel = px.bar(df['fuelType'].value_counts().reset_index(), 
                      x='fuelType', y='count', template="plotly_dark", color='count')
    st.plotly_chart(fig_fuel, use_container_width=True)

with row2_2:
    st.subheader("Price vs Mileage Analysis")
    fig_scatter = px.scatter(df, x='mileage', y='price', color='model', 
                             opacity=0.5, template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

with row2_3:
    st.subheader("Price Range Distribution")
    fig_dist = px.histogram(df, x="price", nbins=20, template="plotly_dark", 
                            color_discrete_sequence=['#00d4ff'])
    st.plotly_chart(fig_dist, use_container_width=True)

# 6. PRICE PREDICTOR SECTION (Fungsi Statistik Terapan)
st.markdown("---")
st.header("🔮 BMW Smart Price Predictor")
p_col1, p_col2 = st.columns([1, 2])

with p_col1:
    st.write("Input spesifikasi untuk estimasi harga:")
    in_mileage = st.number_input("Mileage (Jarak Tempuh)", value=20000)
    in_year = st.slider("Tahun Kendaraan", 2000, 2025, 2018)
    in_engine = st.number_input("Engine Size (L)", value=2.0)
    
    # Simple ML Model (Multiple Regression)
    if len(df) > 10:
        X = df[['mileage', 'year', 'engineSize']]
        y = df['price']
        model = LinearRegression().fit(X, y)
        prediction = model.predict([[in_mileage, in_year, in_engine]])
        
        st.success(f"Estimasi Harga Jual: **£{prediction[0]:,.2f}**")
    else:
        st.warning("Data kurang untuk melakukan prediksi.")

with p_col2:
    st.subheader("Correlation Heatmap")
    corr = df[['price', 'year', 'mileage', 'tax', 'mpg', 'engineSize']].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='Blues', template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)

# 7. RAW DATA TABLE
with st.expander("View Complete Inventory Data"):
    st.dataframe(df, use_container_width=True)
