import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

url_day = "https://raw.githubusercontent.com/fafaa710/dicoding/main/submission/dashboard/day.csv"
url_hour = "https://raw.githubusercontent.com/fafaa710/dicoding/main/submission/dashboard/hour.csv"

# Load data langsung dari GitHub
day_df = pd.read_csv(url_day)
hour_df = pd.read_csv(url_hour)


st.write(
    """
    # Dashboard Peminjaman Sepeda 
    Hello, Selamat datang!
    """
)

# Sidebar
st.sidebar.header("Filter Tanggal Peminjaman")

# Mengatur rentang tanggal berdasarkan data
min_date = datetime.date(2011, 1, 1)
max_date = datetime.date(2012, 12, 1)


# Menampilkan widget date_input di sidebar
selected_date = st.sidebar.date_input("Pilih Tanggal", min_value=min_date, max_value=max_date, value=min_date)


# Membuat 3 kolom
col1, col2, col3 = st.columns(3)

# Menampilkan total peminjaman
with col1:
    total_peminjaman = day_df['cnt'].sum()
    st.metric("Total Peminjaman Sepeda", value=total_peminjaman)

# Menampilkan total registered
with col2:
    total_registered = day_df['registered'].sum()
    st.metric("Total Registered", value=total_registered)

# Menampilkan total casual
with col3:
    total_casual = day_df['casual'].sum()
    st.metric("Total Casual", value=total_casual)


# Judul
st.title("Dashboard Analisis Peminjaman Sepeda")

# 1️⃣ Line Chart: Tren Peminjaman Sepeda
# Konversi kolom tanggal ke format datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Buat kolom baru untuk tahun dan bulan
day_df['year_month'] = day_df['dteday'].dt.to_period('M')  # Format YYYY-MM

# Agregasi jumlah peminjaman per bulan
monthly_trend = day_df.groupby('year_month')['cnt'].sum().reset_index()
monthly_trend['year_month'] = monthly_trend['year_month'].astype(str)  # Ubah ke string untuk ditampilkan

# Visualisasi tren penjualan sepeda per bulan
st.subheader("📊 Tren Pergerakan Penjualan Sepeda per Bulan (2011-2012)")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_trend['year_month'], monthly_trend['cnt'], marker='o', linestyle='-', color='#211C84')

plt.xticks(rotation=45)  # Miringkan label sumbu X agar terbaca jelas
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman")
ax.legend(["Total Peminjaman per Bulan"])

st.pyplot(fig)


# 2️⃣ Pie Chart: Peminjaman Sepeda per Musim
st.subheader("🌦️ Peminjaman Sepeda per Musim")
peminjaman_per_musim = data_day.groupby("season")["cnt"].sum()
fig, ax = plt.subplots()
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
ax.pie(peminjaman_per_musim, labels=[season_mapping[s] for s in peminjaman_per_musim.index], 
       autopct='%1.1f%%', colors=['#211C84', '#4D55CC', '#7A73D1', '#B5A8D5'])
st.pyplot(fig)

# 3️⃣ Stacked Bar Chart: Peminjaman Casual dan Registered per Jam
st.subheader("⏰ Perbandingan Peminjaman Casual dan Registered per Jam")
hourly_data = hour_df.groupby("hr")[["casual", "registered"]].sum()
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(hourly_data.index, hourly_data["casual"], label="Casual", color="#211C84")
ax.bar(hourly_data.index, hourly_data["registered"], bottom=hourly_data["casual"], label="Registered", color="#4D55CC")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
ax.legend()
st.pyplot(fig)

# 4️⃣ Line Chart: Pola Peminjaman Sepeda pada Hari Kerja dan Hari Libur
st.subheader("📆 Pola Peminjaman Sepeda pada Hari Kerja dan Hari Libur per Jam")
pola_peminjaman_per_jam = hour_df.groupby(["hr", "workingday"])["cnt"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
colors = ['#211C84', '#4D55CC']
for i, label in enumerate(["Holiday", "Working Day"]):
    subset = pola_peminjaman_per_jam[pola_peminjaman_per_jam['workingday'] == i]
    ax.plot(subset['hr'], subset['cnt'], label=label, marker='o', color=colors[i])
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
ax.legend()
st.pyplot(fig)

# 5️⃣ Clustering Analysis: Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda
st.subheader("🌬️ Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda")
def windspeed_category(wind):
    if wind < 0.15:
        return "Low"
    elif 0.15 <= wind < 0.30:
        return "Medium"
    else:
        return "High"

hour_df["windspeed_category"] = hour_df["windspeed"].apply(windspeed_category)
windspeed_cluster = hour_df.groupby("windspeed_category")["cnt"].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(x="windspeed_category", y="cnt", data=windspeed_cluster, palette=['#211C84', '#4D55CC', '#7A73D1'], ax=ax)
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

