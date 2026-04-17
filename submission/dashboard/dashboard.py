import streamlit as st
import pandas as pd
import plotly.express as px

# Judul & config
st.set_page_config(page_title="Dashboard Kualitas Udara Beijing", layout="wide")
st.title("Dashboard Analisis Kualitas Udara Beijing")
st.markdown("*Periode Data: 2013-2017 | Sumber: 12 Stasiun Pemantauan*")

# Baca data (pastikan main_data.csv ada di folder yang sama)
@st.cache_data
def load_data():
    return pd.read_csv('main_data.csv')

df = load_data()
df['datetime'] = pd.to_datetime(df['datetime'])

# SIDEBAR: Filter stasiun
st.sidebar.header("Filter")
pilih_stasiun = st.sidebar.multiselect(
    "Pilih Stasiun:",
    options=df['station'].unique(),
    default=df['station'].unique()
)
df_filtered = df[df['station'].isin(pilih_stasiun)]

# METRIK UTAMA
c1, c2, c3 = st.columns(3)
c1.metric("Rata-rata PM2.5", f"{df_filtered['PM2.5'].mean():.1f} µg/m³")
c2.metric("Rata-rata PM10", f"{df_filtered['PM10'].mean():.1f} µg/m³")
c3.metric("Jumlah Record", f"{len(df_filtered):,}")

# GRAFIK 1: Tren Waktu
st.subheader("Tren Polusi per Bulan")
monthly = df_filtered.groupby(df_filtered['datetime'].dt.to_period('M'))[['PM2.5', 'PM10']].mean().reset_index()
monthly['datetime'] = monthly['datetime'].dt.to_timestamp()
fig1 = px.line(monthly, x='datetime', y=['PM2.5', 'PM10'], labels={'value':'Konsentrasi (µg/m³)'})
st.plotly_chart(fig1, use_container_width=True)

# GRAFIK 2: Perbandingan Stasiun
st.subheader("Rata-rata PM2.5 per Stasiun")
station_avg = df_filtered.groupby('station')['PM2.5'].mean().sort_values(ascending=False)
fig2 = px.bar(x=station_avg.index, y=station_avg.values, labels={'x':'Stasiun', 'y':'PM2.5 (µg/m³)'})
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)