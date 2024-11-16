import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set seaborn style
sns.set_theme(style='dark')

# Import data
all_data = pd.read_csv('https://github.com/ridwaanhall/dicoding-bike-sharing-analysis/raw/refs/heads/main/dashboard/main_data.csv')

# Convert date columns to datetime
datetime_columns = ['date']
all_data.sort_values(by='date', inplace=True)
all_data.reset_index(inplace=True)

for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

# Prepare necessary dataframes
def create_month_recap(df):
    df['year_month'] = df['month'].astype(str) + ' ' + df['year'].astype(str)
    df['total_sum'] = df.groupby('year_month')['total'].transform('sum')
    return df[['year_month', 'total_sum']]

def create_season_recap(df):
    return df.groupby('season')[['registered', 'casual']].sum().reset_index()

def create_weather_recap(df):
    return df.groupby('weather').agg({'total': 'mean'}).reset_index()

def create_workingday_hour_recap(df):
    filter_workingday = df[df['workingday'] == 1]
    return filter_workingday.groupby('hour').agg({'total': 'sum'}).reset_index()

def create_holiday_hour_recap(df):
    filter_holiday = df[(df['holiday'] == 1) | (df['workingday'] == 0)]
    return filter_holiday.groupby('hour').agg({'total': 'sum'}).reset_index()

def create_rfm_recap(df):
    rfm_df = df.groupby('hour', as_index=False).agg({
        'date': 'max',
        'instant': 'nunique',
        'total': 'sum'
    })
    rfm_df.columns = ['hour', 'last_order_date', 'order_count', 'revenue']
    rfm_df['last_order_date'] = rfm_df['last_order_date'].dt.date
    recent_date = df['date'].dt.date.max()
    rfm_df['recency'] = rfm_df['last_order_date'].apply(lambda x: (recent_date - x).days)
    rfm_df.drop('last_order_date', axis=1, inplace=True)
    return rfm_df

def create_daily_recap(df):
    return df.groupby('date').agg({'total': 'sum'}).reset_index()

def create_registered_recap(df):
    return df.groupby('date').agg({'registered': 'sum'}).reset_index()

def create_casual_recap(df):
    return df.groupby('date').agg({'casual': 'sum'}).reset_index()

def create_temp_recap(df):
    return df.groupby('date').agg({'temp': 'mean'}).reset_index()

def create_hum_recap(df):
    return df.groupby('date').agg({'hum': 'mean'}).reset_index()

# Create date filter in sidebar
max_date = pd.to_datetime(all_data['date']).dt.date.max()
min_date = pd.to_datetime(all_data['date']).dt.date.min()

with st.sidebar:
    st.image('https://raw.githubusercontent.com/ridwaanhall/dicoding-bike-sharing-analysis/main/dashboard/analytics.png')

    # Input start_date and end_date
    start_date, end_date = st.date_input(
        label='Select Date Range',
        max_value=max_date,
        min_value=min_date,
        value=[min_date, max_date]
    )
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)
    
    st.title('Created by:')
    st.write(
        """ 
        **RIDWAN HALIM**\n
        Dicoding ID: **ridwaanhall**\n
        Email: **ridwaanhall.dev@gmail.com**
        """
    )

main_df = all_data[(all_data['date'] >= str(start_date)) & 
                   (all_data['date'] <= str(end_date))]

month_recap_df = create_month_recap(main_df)
season_recap_df = create_season_recap(main_df)
weather_recap_df = create_weather_recap(main_df)
workingday_hour_recap_df = create_workingday_hour_recap(main_df)
holiday_hour_recap_df = create_holiday_hour_recap(main_df)
rfm_recap_df = create_rfm_recap(main_df)
daily_recap_df = create_daily_recap(main_df)
casual_recap_df = create_casual_recap(main_df)
registered_recap_df = create_registered_recap(main_df)
temp_recap_df = create_temp_recap(main_df)
hum_recap_df = create_hum_recap(main_df)

# Create UI
st.header('BIKE SHARING ANALYTICS DASHBOARD')

# Subheader Rent Summary
st.subheader('BIKE SHARING Rent Summary')
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    daily_recap = daily_recap_df['total'].sum()
    st.metric('Total User', value=daily_recap)

with col2:
    registered_recap = registered_recap_df['registered'].sum()
    st.metric('Registered User', value=registered_recap)

with col3:
    casual_recap = casual_recap_df['casual'].sum()
    st.metric('Casual User', value=casual_recap)

with col4:
    temp_recap = (temp_recap_df['temp'].mean() * 41).round(2)
    st.metric('Mean Temp (°C)', value=str(temp_recap) + '°C')

with col5:
    hum_recap = (hum_recap_df['hum'].mean() * 100).round(2)
    st.metric('Mean Humidity (%)', value=str(hum_recap) + '%')

# Subheader Monthly Recap
st.subheader('Monthly Rent Recap')
fig, ax = plt.subplots(figsize=(16, 8))
colors = sns.color_palette("husl", len(month_recap_df['year_month']))
ax.bar(
    month_recap_df['year_month'],
    month_recap_df['total_sum'],
    color=colors
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)
ax.set_title('Monthly Rent Recap', fontsize=25)
ax.set_xlabel('Year Month', fontsize=20)
ax.set_ylabel('Total Sum', fontsize=20)

st.pyplot(fig)

# Subheader Season and Weather Recap
st.subheader('Season and Weather Recap')
 
col1, col2 = st.columns(2)
 
with col1:
    seasonal_totals = main_df.groupby('season')[['registered', 'casual']].sum().reset_index()
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        data=seasonal_totals, 
        x='season', 
        y='registered', 
        label='Registered', 
        color='skyblue',
        ax=ax
    )
    sns.barplot(
        data=seasonal_totals, 
        x='season', 
        y='casual', 
        label='Casual', 
        color='lightcoral',
        ax=ax
    )
    ax.set_title('Total Bike Rentals by Season', loc='center', fontsize=50)
    ax.set_xlabel('Season', fontsize=35)
    ax.set_ylabel('Total Rentals', fontsize=35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.legend(fontsize=20)
    st.pyplot(fig)

with col2:
    plot_weather = main_df.groupby(by='weather').agg({
        'total': 'mean'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=plot_weather, 
        x='weather', 
        y='total',
        palette='viridis',
        ax=ax
    )
    ax.set_xlabel('Weather Condition', fontsize=12)
    ax.set_ylabel('Average Total Rentals', fontsize=12)
    ax.set_title('Average Bike Rentals Weather Condition', fontsize=14)
    ax.tick_params(axis='x', labelsize=12, rotation=45)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

# Subheader Workingday and Holiday Hour Recap
st.subheader('Workingday and Holiday Hour Recap')
 
col1, col2 = st.columns(2)
 
with col1:
    plot_hour_workingday = workingday_hour_recap_df.groupby('hour').agg({
        'total': 'sum'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    # Determine the indices of the columns with the three highest totals
    top_3_cols = plot_hour_workingday['total'].nlargest(3).index

    sns.barplot(
        data=plot_hour_workingday, 
        x='hour', 
        y='total',
        color='tab:blue',
        ax=ax
    )

    # Highlight the top 3 columns in red
    for col in top_3_cols:
        ax.bar(col, plot_hour_workingday.loc[col, 'total'], color='tab:red', label='Top 3 Hours' if col == top_3_cols[0] else "")

    ax.set_title("Total Bike Rentals by Hour on Working Days")
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Total Rentals')
    ax.legend()
    st.pyplot(fig)

with col2:
    plot_hour_holiday = holiday_hour_recap_df.groupby(by='hour').agg({
        'total': 'sum'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    top_5_cols = plot_hour_holiday['total'].nlargest(5).index

    sns.barplot(
        data=plot_hour_holiday, 
        x='hour', 
        y='total',
        color='tab:blue',
        ax=ax
    )

    for col in top_5_cols:
        ax.bar(col, plot_hour_holiday.loc[col, 'total'], color='tab:red', label='Top 5 Hours' if col == top_5_cols[0] else "")

    ax.set_title("Total Bike Rentals by Hour on Holidays")
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Total Rentals')
    ax.legend()
    st.pyplot(fig)

# Subheader RFM Recap
st.subheader('RFM Recap')

col1, col2, col3 = st.columns(3)

# Sort the RFM data
top_recency = rfm_recap_df.sort_values(by="recency", ascending=True).head(5)
top_frequency = rfm_recap_df.sort_values(by="order_count", ascending=False).head(5)
top_monetary = rfm_recap_df.sort_values(by="revenue", ascending=False).head(5)

# Create subplots
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 24))

sns.barplot(
    data=top_recency, 
    x="hour", 
    y="recency",
    palette='Blues_d',
    ax=ax[0]
)
ax[0].set_ylabel("Recency (days)", fontsize=14)
ax[0].set_xlabel("Hour", fontsize=14)
ax[0].set_title("Top 5 Hours by Recency", fontsize=18)
ax[0].tick_params(axis='x', labelsize=12)
ax[0].tick_params(axis='y', labelsize=12)

# Plot top frequency
sns.barplot(
    data=top_frequency,
    x="hour",
    y="order_count", 
    palette='Greens_d',
    ax=ax[1]
)
ax[1].set_ylabel("Frequency", fontsize=14)
ax[1].set_xlabel("Hour", fontsize=14)
ax[1].set_title("Top 5 Hours by Frequency", fontsize=18)
ax[1].tick_params(axis='x', labelsize=12)
ax[1].tick_params(axis='y', labelsize=12)

# Plot top monetary
sns.barplot(
    data=top_monetary, 
    x="hour", 
    y="revenue", 
    palette='Reds_d',
    ax=ax[2]
)
ax[2].set_ylabel("Monetary", fontsize=14)
ax[2].set_xlabel("Hour", fontsize=14)
ax[2].set_title("Top 5 Hours by Monetary Value", fontsize=18)
ax[2].tick_params(axis='x', labelsize=12)
ax[2].tick_params(axis='y', labelsize=12)

# Set the overall title
plt.suptitle("Best Rental Hours Based on RFM Parameters", fontsize=22, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
st.pyplot(fig)

st.markdown('<div style="text-align: center; padding: 10px 0; font-size: 12px;">Copyright (c) ridwaanhall 2024</div>', unsafe_allow_html=True)
