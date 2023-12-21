import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re
sns.set(style='dark')

df = pd.read_csv("day.csv")
df.dteday = pd.to_datetime(df.dteday)
df.sort_values(by='dteday', inplace=True)

min_date = df.dteday.min()
max_date = df.dteday.max()

with st.sidebar:
    st.image("Bike Station.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header("Bike Share Performance")

main_df = df[(df["dteday"] >= str(start_date)) &
             (df["dteday"] <= str(end_date))]

day_dict = {0: 'Sunday',
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday'}
season_dict = {1: 'musim semi',
               2: 'musim panas',
               3: 'musim gugur',
               4: 'musim dingin'}
weather_dict = {1: 'cerah',
                2: 'kabut',
                3: 'gerimis',
                4: 'hujan deras'}

main_df['day_sorter'] = main_df['weekday']
main_df['weekday'] = main_df['weekday'].replace(day_dict)
main_df['season'] = main_df['season'].replace(season_dict)
main_df['weathersit'] = main_df['weathersit'].replace(weather_dict)
st.subheader("Daily User Average")

col1, col2, col3 = st.columns(3)
with col1:
    casual = main_df.casual.mean()
    st.metric("Casual", value=round(casual, 2))

with col2:
    registered = main_df.registered.mean()
    st.metric("Registered", value=round(registered, 2))

with col3:
    count = main_df.cnt.mean()
    st.metric("Total Users in Average", value=round(count, 2))

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x='dteday', y='cnt', data=main_df)
ax.set_title("Trend Line")
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x='dteday', y='cnt', hue='season', data=main_df)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Breakdown by Season", loc="center", fontsize=15)
st.pyplot(fig)

# Highest
st.subheader("A Day with The Highest Count of Users")
col1, col2, col3, col4 = st.columns(4)
highest_cnt = main_df[main_df['cnt'] == main_df['cnt'].max()]

with col1:
    st.metric("Count", value=highest_cnt['cnt'])

with col2:
    st.metric("Date", value=str(
        (str(highest_cnt['dteday'].values).split("T")[0].lstrip("['"))))

with col3:
    st.metric("Day", value=str(
        highest_cnt['weekday'].values).lstrip("['").rstrip("']'"))

with col4:
    st.metric("Weather", value=str(
        highest_cnt['weathersit'].values).lstrip("['").rstrip("']'"))

# Highest second row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Holiday?", value="No" if int(
        highest_cnt['holiday']) == 0 else "Yes")

with col2:
    st.metric("Temp (in Celcius)", value=round(highest_cnt['temp']*41, 1))

with col3:
    st.metric("Humidity", value=round(highest_cnt['hum']*100, 1))

with col4:
    st.metric("Windspeed", value=round(highest_cnt['windspeed']*67, 1))

# Lowest
st.subheader("A Day with The Lowest Count of Users")
col1, col2, col3, col4 = st.columns(4)
lowest_cnt = main_df[main_df['cnt'] == main_df['cnt'].min()]
with col1:
    st.metric("Count", value=lowest_cnt['cnt'])

with col2:
    st.metric("Date", value=str(
        (str(lowest_cnt['dteday'].values).split("T")[0].lstrip("['"))))

with col3:
    st.metric("Day", value=str(
        lowest_cnt['weekday'].values).lstrip("['").rstrip("']'"))

with col4:
    st.metric("Weather", value=str(
        lowest_cnt['weathersit'].values).lstrip("['").rstrip("']'"))

# Lowest 2nd rows
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Holiday?", value="No" if int(
        lowest_cnt['holiday']) == 0 else "Yes")

with col2:
    st.metric("Temp (in Celcius)", value=round(lowest_cnt['temp']*41, 1))

with col3:
    st.metric("Humidity", value=round(lowest_cnt['hum']*100, 1))

with col4:
    st.metric("Windspeed", value=round(lowest_cnt['windspeed']*67, 1))

# Highest Weekday Visualization
st.subheader("Highest Rent Grouped by Day")
sum_weekday = main_df.groupby(
    ['day_sorter', 'weekday']).cnt.sum().reset_index()
mean_weekday = main_df.groupby(
    ['day_sorter', 'weekday']).cnt.mean().reset_index()
median_weekday = main_df.groupby(
    ['day_sorter', 'weekday']).cnt.median().reset_index()

fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(data=sum_weekday.sort_values(by='day_sorter'),
            x='weekday', y='cnt',
            label='Count Sum',
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "green", "#D3D3D3"]
           )
plt.xlabel(None)
plt.ylabel(None)
for x, y in zip(range(0, 7), sum_weekday['cnt']):
    plt.text(x, y, str(y), ha='center', va='bottom', fontsize=12)
plt.title("Sum of Users")
st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

sns.barplot(data=mean_weekday.sort_values(by='day_sorter'),
            x='weekday', y='cnt',
            label='Count Mean', ax=ax[0],
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "green", "#D3D3D3"]
           )
ax[0].set_title("Mean of Users")
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
for x, y in zip(range(7), mean_weekday['cnt']):
    ax[0].text(x, y, str(int(y)), ha='center', va='bottom', fontsize=12)

sns.barplot(data=median_weekday.sort_values(by='day_sorter'),
            x='weekday', y='cnt',
            label='Count Median', ax=ax[1],
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",  "green", "#D3D3D3", "#D3D3D3"]
           )
ax[1].set_title("Median of Users")
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
for x, y in zip(range(7), median_weekday['cnt']):
    ax[1].text(x, y, str(int(y)), ha='center', va='bottom', fontsize=12)
st.pyplot(fig)

# Correlation Visualization
st.subheader(
    "Correlation Between Columns with Floating Data Type to The Count of Rent")
corr = main_df[['temp', 'atemp', 'hum', 'windspeed', 'casual',
                'registered', 'cnt']].corr()[['casual', 'registered', 'cnt']]
fig, ax = plt.subplots(figsize=(4, 3))
sns.heatmap(corr, annot=True, cmap='YlGnBu')
st.pyplot(fig)

st.caption("NormanFebrioooOooOOO")
