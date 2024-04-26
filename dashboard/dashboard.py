import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='whitegrid')

# Membuat judul
st.header(' Analisa Data Rental Sepeda 🚴‍♀️')
st.markdown(''' Keterangan:
        - instan: rekor indeks
    - dteday : tanggal
    - season : musim
    - yr : tahun (0: 2011, 1:2012)
    - mnth: bulan (1 hingga 12)
    - hr : jam (0 hingga 23)
    - holiday : hari cuaca libur atau tidak (disarikan dari http://dchr.dc.gov/page/holiday-schedule)
    - weekday : hari dalam seminggu
    - working day : jika hari bukan akhir pekan atau hari libur adalah 1, sebaliknya adalah 0.
    - cuaca :
		- 1: Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian
        - 2: Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
        - 3: Salju Ringan, Hujan Ringan + Badai Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar
        - 4: Hujan Lebat + Palet Es + Badai Petir + Kabut, Salju + Kabut
	- atemp : Menormalkan suhu perasaan dalam Celsius. Nilainya dibagi 50 (maks)
    - hum: Kelembapan yang dinormalisasi. Nilainya dibagi menjadi 100 (maks)
    - Kecepatan Angin: Kecepatan angin yang dinormalisasi. Nilainya dibagi menjadi 67 (maks)
    - santai: jumlah pengguna biasa
    - terdaftar: jumlah pengguna terdaftar
    - cnt: hitungan total sewa sepeda termasuk sepeda kasual dan terdaftar''')
st.subheader('Cek Data Rental Berdasarkan Bulan dan Tahun')

# Mencoba Menampilkan Data Tabular dengan Filter bulan dan hari
def load_data(file_path):
    data = pd.read_csv(file_path)
    # Convert 'dteday' column to datetime type
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

# Load CSV file
file_path = "hour.csv"
data = load_data(file_path)

# Create filters for year and month
tahun = sorted(data['dteday'].dt.year.unique())
selected_year = st.selectbox('Pilih Tahun:', tahun)

bulan = sorted(data['dteday'].dt.month.unique())
selected_month = st.selectbox('Pilih Bulan:', bulan)

# Filter data based on selected year and month
filtered_data = data[(data['dteday'].dt.year == selected_year) & 
                     (data['dteday'].dt.month == selected_month)]

# Show filtered data
st.write(filtered_data)

# Menyiapkan data day_df dan hour_df
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")
day_df.head()

# Mengubah beberapa keterangan kolom
day_df['month'] = day_df['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Mengubah beberapa keterangan hour_df
hour_df['hour'] = hour_df['hr'].map({
    0: '12am',1: '1am', 2: '2am', 3: '3am', 4: '4am', 5: '5am', 6: '6am',
    7: '7am', 8: '8am', 9: '9am', 10: '10am', 11: '11am', 12: '12pm', 13: '1pm', 14: '2pm', 15: '3pm', 16:'4pm', 17:'5pm', 18:'6pm', 19:'7pm', 20:'8pm', 21:'9pm', 22:'10pm', 23:'11pm'
})


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['cnt','registered']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='mnth')[['cnt','registered']].sum().reset_index()
    monthly_rent_df['month'] = monthly_rent_df['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'cnt': 'sum'
    })
    return weather_rent_df

# hourly_df
def create_hourly_df(df):
    hourly_rent_df = hour_df.groupby(by='hour').agg({
        'cnt': 'sum'
    })
    return hourly_rent_df

# Membuat komponen filter dengan rentang
min_date = pd.to_datetime(day_df['dteday']).dt.date.min()
max_date = pd.to_datetime(day_df['dteday']).dt.date.max()
 
with st.sidebar:
    st.image('1.png')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

#main_df day_df
main_df = day_df[(day_df['dteday'] >= str(start_date)) & 
                (day_df['dteday'] <= str(end_date))]

#main_df hour_df
main_hour_df = day_df[(day_df['dteday'] >= str(start_date)) & 
                (day_df['dteday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
hourly_rent_df = create_hourly_df(main_hour_df)
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat jumlah penyewaan harian
st.subheader('Data Rental by Filter')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Pengguna Kasual', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Pengguna Terdaftar', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total Pengguna', value= daily_rent_total)

# Membuat plot jumlah penyewa paling banyak dalam jam tertentu
st.subheader('Jumlah Penyewa Pada Jam Tertentu')
fig, ax = plt.subplots(figsize=(24, 8))

sns.barplot(
    x=hourly_rent_df.index,
    y=hourly_rent_df['cnt'],
    color='tab:blue'
)

for index, row in enumerate(hourly_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan Musim
st.subheader('Jumlah Penyewa Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    # adalah indeks dari season_rent_df
    x=['spring', 'summer', 'fall', 'winter'],
    y=season_rent_df['cnt'],
    palette=colors,
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['cnt'], str(row['cnt']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel("Musim (0:springer, 1:summer, 2:fall, 3:winter)")
ax.set_ylabel("Jumlah Penyewa")
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

st.subheader('Jumlah Penyewa Berdasarkan bulan')
fig, ax = plt.subplots(figsize=(24, 8))

sns.barplot(
    x=monthly_rent_df['month'],  # Menggunakan column bulan dari DataFrame
    y=monthly_rent_df['cnt'],
    color='tab:blue',
    data=monthly_rent_df,
    ax=ax
)

for index, row in enumerate(monthly_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Data Persewaan Saat Hari Kerja dan Liburan')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors1=["tab:blue", "tab:red"]
colors2=["tab:blue", "tab:red"]
colors3=["tab:blue", "tab:pink", "tab:red", "tab:green", "tab:orange", "tab:pink", "tab:brown"]

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='cnt',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['cnt']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Banyaknya penyewa berdasarkan hari kerja')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='cnt',
  data=holiday_rent_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_rent_df['cnt']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Jumlah Penyewa Saat Liburan')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='cnt',
  data=weekday_rent_df,
  palette=colors3,
  ax=axes[2])

for index, row in enumerate(weekday_rent_df['cnt']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Jumlah Penyewa Setiap Hari')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)