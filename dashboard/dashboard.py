import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load dataset dengan caching
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/aotizhongxin_data.csv", parse_dates=["date"])
    df["year"] = df["date"].dt.year
    df["hour"] = df["date"].dt.hour
    return df

df = load_data()

# Sidebar
st.sidebar.title("Kualitas Udara Aotizhongxin Station")
st.sidebar.write("**Oleh:** Cut Nabilah Putri Ulanty")
st.sidebar.write("**Student ID:** MC319D5X2391")

# rentang tanggal dari dataset
min_date = df["date"].min().date()
max_date = df["date"].max().date()

# Set min_date ke 1 Januari 2013 karena data dimulai dari tahun 2013 di datastr
if min_date.year == 2013:
    min_date = datetime.date(2013, 1, 1)

if "selected_date" not in st.session_state:
    st.session_state.selected_date = None  # Awalnya None

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

# Tanggal yang dipilih nantinya akan disimpan ke session_state
if selected_date is not None:
    st.session_state.selected_date = selected_date
else:
    selected_date = None  #Menampilkan tampilan dashboard awal

pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
weather_factors = ["TEMP", "RAIN", "PRES", "DEWP", "WSPM"]

# **Tampilan awal dashboard**
if selected_date is None:
    st.title("Kualitas Udara Aotizhongxin Station (2013-2017)")

    # **Grafik kualitas udara periode 2013-2017**
    fig, ax = plt.subplots()
    aqiyearly = df.groupby("year")["AQI"].mean()
    sns.barplot(x=aqiyearly.index, y=aqiyearly.values, ax=ax)
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata AQI")
    ax.set_title("Rata-rata AQI per Tahun")
    st.pyplot(fig)

    # **Grafik kadar zat polutan tiap tahunnya**
    fig, ax = plt.subplots()
    pollutant_yearly = df.groupby("year")[pollutants].mean()
    pollutant_yearly.plot(kind="bar", stacked=True, ax=ax)
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Kadar Polutan")
    ax.set_title("Kadar Zat Polutan per Tahun")
    st.pyplot(fig)

    # **Grafik rata-rata kualitas udara per jam (2013-2017)**
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="hour", y="AQI", hue="year", marker="o", ax=ax, palette="tab10", ci=20)
    ax.set_xlabel("Jam")
    ax.set_ylabel("AQI")
    ax.set_title("Rata-rata Kualitas Udara per Jam (2013-2017)")
    ax.legend(title="Tahun")
    ax.set_xticks(range(0, 24, 1))
    ax.set_xticklabels([f"{h % 12 or 12}{'AM' if h < 12 else 'PM'}" for h in range(0, 24)], rotation=45)
    st.pyplot(fig)

    # **Grafik hubungan AQI dengan faktor cuaca**
    fig, ax = plt.subplots()
    df[weather_factors + ["AQI"]].corr()["AQI"].drop("AQI").plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Faktor Cuaca")
    ax.set_ylabel("Korelasi dengan AQI")
    ax.set_title("Hubungan AQI dengan Faktor Cuaca")
    st.pyplot(fig)

    # Menambahkan keterangan mengenai grafik
    st.write("""
    **Keterangan :**
    - **TEMP : suhu**
    - **RAIN : curah hujan**
    - **PRES : Tekanan udara**
    - **DEWP : dew point / titik embun**
    - **WSPM : wind speed / kecepatan angin**
             
    **Interpretasi Grafik:**
    - **Nilai positif (di atas 0)** → Faktor cuaca meningkat, AQI juga meningkat (polusi lebih tinggi / kualitas udara buruk).
    - **Nilai negatif (di bawah 0)** → Faktor cuaca meningkat, AQI menurun (polusi turun / kualitas udara baik).
    """)

    # **Dropdown rentang kategori kualitas udara /AQI**
    with st.expander("Status Kualitas Udara (AQI)"): 
        st.write("* 0-50: Baik\n* 51-100: Sedang\n* 101-150: Tidak sehat bagi kelompok sensitif\n* 151-200: Tidak sehat\n* 201-300: Sangat tidak sehat\n* >300: Berbahaya")
    

# **Tampilan saat tanggal dipilih**
else:
    st.title(f"Kualitas Udara pada {selected_date.strftime('%Y-%m-%d')}")
    
    # **Memastikan format tanggal cocok dengan dataset**
    selected_date = pd.to_datetime(selected_date)
    selected_data = df[df["date"].dt.date == selected_date.date()]

    # Cek jika tanggal yang dipilih sebelum 1 Maret 2013
    if selected_date.year == 2013 and selected_date.month < 3:
        st.warning("Data dimualai dari 01 Maret 2013")
    elif not selected_data.empty:
        # **Grafik AQI pada tanggal yang dipilih**
        fig, ax = plt.subplots()
        sns.barplot(x=[selected_date.strftime('%Y-%m-%d')], y=[selected_data["AQI"].mean()], ax=ax, color="blue")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("AQI")
        ax.set_title(f"AQI pada {selected_date.strftime('%Y-%m-%d')}")
        st.pyplot(fig)

        # **Grafik kandungan zat polutan pada tanggal yang dipilih**
        fig, ax = plt.subplots()
        selected_data[pollutants].mean().plot(kind="bar", ax=ax, color="orange")
        ax.set_xlabel("Jenis Polutan")
        ax.set_ylabel("Kadar")
        ax.set_title("Kandungan Zat Polutan")
        st.pyplot(fig)

        # **Grafik AQI berdasarkan jam**
        hourly_data = selected_data.groupby("hour")["AQI"].mean()

        # **Grafik performa kualitas udara berdasarkan jam**
        fig, ax = plt.subplots()
        sns.lineplot(x=hourly_data.index, y=hourly_data.values, ax=ax, color="red", marker="o")
        ax.set_xlabel("Jam")
        ax.set_ylabel("AQI")
        ax.set_title("Performa Kualitas Udara Berdasarkan Jam")
        ax.set_xticks(range(0, 24, 1))
        ax.set_xticklabels([f"{h % 12 or 12}{'AM' if h < 12 else 'PM'}" for h in range(0, 24)], rotation=45)
        st.pyplot(fig)

        # **Dropdown rentang kategori kualitas udara /AQI**
        with st.expander("Status Kualitas Udara (AQI)"): 
            st.write("* 0-50: Baik\n* 51-100: Sedang\n* 101-150: Tidak sehat bagi kelompok sensitif\n* 151-200: Tidak sehat\n* 201-300: Sangat tidak sehat\n* >300: Berbahaya")
    else:
        st.warning(f"Tidak ada data untuk tanggal {selected_date.strftime('%Y-%m-%d')}.")