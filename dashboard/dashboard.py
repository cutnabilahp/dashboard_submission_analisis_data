import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/aotizhongxin_data.csv", parse_dates=["date"])
    df["year"] = df["date"].dt.year
    df["hour"] = df["hour"].astype(str).str[:2].astype(int)
    return df

df = load_data()

# Sidebar
st.sidebar.title("Kualitas Udara Aotizhongxin Station")
st.sidebar.write("**Oleh:** Cut Nabilah Putri Ulanty")
st.sidebar.write("**Student ID:** MC319D5X2391")

# Rentang tanggal dari dataset
min_date = df["date"].min().date()
max_date = df["date"].max().date()
if min_date.year == 2013:
    min_date = datetime.date(2013, 1, 1)

# Widget kalender
selected_date = st.sidebar.date_input(
    "Pilih Tanggal",
    value=None,
    min_value=min_date,
    max_value=max_date,
    key="date_picker",
    format="YYYY/MM/DD",
    help="Silakan pilih tanggal"
)

pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
weather_factors = ["TEMP", "RAIN", "PRES", "DEWP", "WSPM"]

# Tampilan awal dashboard
if selected_date is None:
    st.title("Analisis Kualitas Udara Aotizhongxin (2013-2017)")
    
    # Grafik Tren AQI Tahunan
    st.subheader("Tren Rata-rata AQI per Tahun")
    
    # Menghitung rata-rata AQI per tahun
    aqi_per_year = df.groupby("year")["AQI"].mean()

    # Visualisasi rata-rata AQI
    fig, ax = plt.subplots(figsize=(8, 5))
    aqi_per_year.plot(kind="bar", color="skyblue", edgecolor="black", ax=ax)

    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata AQI")
    ax.set_title("Rata-rata AQI per Tahun (2013-2017)")
    ax.set_xticks(range(len(aqi_per_year.index)))
    ax.set_xticklabels(aqi_per_year.index, rotation=0)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)
    
    #Distribusi Polutan Tahunan
    st.subheader("Distribusi Polutan per Tahun")

    # Hitung rata-rata kadar polutan per tahun
    yearly_avg_pollutants = df.groupby("year")[pollutants].mean()

    # Visualisasi distribusi polutan tahunan
    fig, ax = plt.subplots(figsize=(12, 6))
    yearly_avg_pollutants.plot(kind="bar", figsize=(12, 6), colormap="viridis", ax=ax)

    ax.set_xlabel("Tahun", fontsize=12)
    ax.set_ylabel("Kadar Rata-rata Polutan", fontsize=12)
    ax.set_title("Rata-rata Kadar Polutan per Tahun (2013-2017)", fontsize=14)
    ax.set_xticklabels(yearly_avg_pollutants.index, rotation=0)
    ax.legend(title="Polutan")
    st.pyplot(fig)
    
    # Rata Rata AQI Berdasarkan Jam dari tahun 2013-2017
    st.subheader("Rata-rata AQI Berdasarkan Jam (2013-2017)")

    #rata-rata AQI per jam untuk masing-masing tahun
    aqi_per_hour = df.groupby(["year", "hour"])["AQI"].mean().reset_index()

    #Mengubah format hour menjadi string dengan AM/PM
    hour_labels = [f"{h % 12 if h % 12 != 0 else 12}{'AM' if h < 12 else 'PM'}" for h in range(24)]
    custom_colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FFC300"]  # Warna unik untuk setiap tahun

    fig, ax = plt.subplots(figsize=(12, 6))

    # Membedakan warna line plot untuk setiap tahun
    sns.lineplot(data=aqi_per_hour, x="hour", y="AQI", hue="year", marker="o", palette=custom_colors)
    ax.set_xticks(range(24))
    ax.set_xticklabels(hour_labels, rotation=45)  # Format label jam AM/PM
    ax.set_xlabel("Jam")
    ax.set_ylabel("AQI")
    ax.set_title("Rata-rata Kualitas Udara per Jam (2013-2017)")
    ax.legend(title="Tahun")
    ax.grid(True, linestyle="--", alpha=0.7)
    st.pyplot(fig)
    
    # **Hubungan AQI dengan Faktor Cuaca**
    st.subheader("Korelasi AQI dengan Faktor Cuaca")

    # Pilih hanya kolom numerik dan menghitung korelasi
    corr_matrix = df.select_dtypes(include=["number"]).corr()

    # Memilih faktor cuaca dan mengambil korelasinya dnegan AQI
    weather_factors = ["TEMP", "RAIN", "PRES", "DEWP", "WSPM"]
    weather_corr = corr_matrix.loc[weather_factors, "AQI"]

    # Membuat grafik
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(weather_factors, weather_corr, color="skyblue")
    ax.set_xlabel("Faktor Cuaca")
    ax.set_ylabel("Korelasi dengan AQI")
    ax.set_title("Hubungan AQI dengan Faktor Cuaca")
    ax.axhline(0, color="black", linewidth=0.8)  # Garis tengah
    st.pyplot(fig)

    # Expander untuk status kualitas udara
    with st.expander("Status Kualitas Udara (AQI)"): 
        st.write("* 0-50: Baik\n* 51-100: Sedang\n* 101-150: Tidak sehat bagi kelompok sensitif\n* 151-200: Tidak sehat\n* 201-300: Sangat tidak sehat\n* >300: Berbahaya")


# **Tampilan saat tanggal spesifik dipilih**
else:
    st.title(f"Kualitas Udara pada {selected_date.strftime('%Y-%m-%d')}")
    selected_date = pd.to_datetime(selected_date)
    selected_data = df[df["date"].dt.date == selected_date.date()]

    if selected_date.year == 2013 and selected_date.month < 3:
        st.warning("Data dimulai dari 01 Maret 2013")
    elif not selected_data.empty:
        # Grafik AQI pada tanggal yang dipilih
        st.subheader("AQI pada Tanggal yang Dipilih")
        aqi_mean = selected_data["AQI"].mean()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=[selected_date.strftime('%Y-%m-%d')], y=[aqi_mean], ax=ax, color="#1f77b4", edgecolor="black")
        ax.set_xlabel("Tanggal", fontsize=12, fontweight="bold")
        ax.set_ylabel("AQI", fontsize=12, fontweight="bold")
        ax.set_ylim(0, 100)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)
        
        # **Kandungan Zat Polutan pada tanggal yang dipilih**
        st.subheader("Kandungan Zat Polutan")
        pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
        pollutant_means = selected_data[pollutants].mean()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=pollutant_means.index, y=pollutant_means.values, ax=ax, palette="Oranges", edgecolor="black")
        ax.set_xlabel("Jenis Polutan", fontsize=12, fontweight="bold")
        ax.set_ylabel("Kadar", fontsize=12, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)
        
        # **Performa Kualitas Udara (AQI) Berdasarkan Jam**
        st.subheader("Performa Kualitas Udara Berdasarkan Jam")
        hourly_data = selected_data.groupby("hour")["AQI"].mean()
        hour_labels = [f"{h}:00" for h in range(24)]  

        fig, ax = plt.subplots(figsize=(6, 4)) 
        sns.lineplot(x=hourly_data.index, y=hourly_data.values, ax=ax, color="red", marker="o", linestyle="-", linewidth=2, markersize=6)
        ax.set_xticks(range(24))
        ax.set_xticklabels(hour_labels, rotation=45, fontsize=10)
        ax.set_xlabel("Jam", fontsize=12, fontweight="bold")
        ax.set_ylabel("AQI", fontsize=12, fontweight="bold")
        ax.grid(axis="both", linestyle="--", alpha=0.7)
        st.pyplot(fig)
        
        # Korelasi AQI dengan Faktor Cuaca per Hari
        st.subheader("Korelasi AQI dengan Faktor Cuaca")

        # Korelasi hanya untuk tanggal yang dipilih
        numeric_columns = selected_data.select_dtypes(include=["number"]).columns
        corr_matrix_daily = selected_data[numeric_columns].corr()

        # Mengambil korelasi AQI dengan faktor cuaca
        weather_corr_daily = corr_matrix_daily.loc[weather_factors, "AQI"]

        #Visualisasi korelasi harian
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(weather_corr_daily.index, weather_corr_daily.values, color="skyblue", edgecolor="skyblue")

        ax.set_xlabel("Faktor Cuaca", fontsize=12, fontweight="bold")
        ax.set_ylabel("Korelasi dengan AQI", fontsize=12, fontweight="bold")
        ax.set_title(f"Korelasi AQI dengan Faktor Cuaca ({selected_date.strftime('%Y-%m-%d')})", fontsize=14)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        st.pyplot(fig)

        # Expander untuk status kualitas udara
        with st.expander("Status Kualitas Udara (AQI)"): 
            st.write("* 0-50: Baik\n* 51-100: Sedang\n* 101-150: Tidak sehat bagi kelompok sensitif\n* 151-200: Tidak sehat\n* 201-300: Sangat tidak sehat\n* >300: Berbahaya")
    else:
        st.warning(f"Tidak ada data untuk tanggal {selected_date.strftime('%Y-%m-%d')}.")