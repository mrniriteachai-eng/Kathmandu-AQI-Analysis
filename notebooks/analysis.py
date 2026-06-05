
# STEP 1: Libraries import गरु
# ============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

print("✓ सब libraries load भयो!")

# ============================================
# STEP 2: Data load गरु
# ============================================
df = pd.read_csv('../data/kathmandu_aqi.csv')

# Data को पहिलो 5 rows हेरु
print("\n=== DATA को पहिलो 5 rows ===")
print(df.head())

# Data को shape हेरु (कति rows, कति columns)
print(f"\nडेटा size: {df.shape[0]} rows, {df.shape[1]} columns")

# Data info
print("\n=== DATA INFO ===")
print(df.info())

# ============================================
# STEP 3: Basic Statistics calculate गरु
# ============================================
print("\n=== AQI STATISTICS ===")
print(df['AQI'].describe())

# Using NumPy
aqi_array = np.array(df['AQI'])
print(f"\nAverage AQI: {np.mean(aqi_array):.2f}")
print(f"Median AQI: {np.median(aqi_array):.2f}")
print(f"Std Dev: {np.std(aqi_array):.2f}")
print(f"Max AQI: {np.max(aqi_array)}")
print(f"Min AQI: {np.min(aqi_array)}")

# ============================================
# STEP 4: Simple Visualization
# ============================================
print("\n✓ Graphs बनाइँदै...")

# Graph 1: AQI Line Chart
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['AQI'], marker='o', color='red', linewidth=2)
plt.xlabel('Days', fontsize=12)
plt.ylabel('AQI Level', fontsize=12)
plt.title('Kathmandu Air Quality (AQI)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../output/aqi_line_chart.png', dpi=300)  # Save गरु
plt.show()

print("✓ Line chart saved!")









# ============================================
# ADVANCED ANALYSIS
# ============================================

# 1. Category बनाऊ (AQI Level)
print("\n=== AQI CATEGORIES ===")

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good (हरियो)"
    elif aqi <= 100:
        return "Moderate (पहेलो)"
    elif aqi <= 150:
        return "Unhealthy for Sensitive (नारंगी)"
    elif aqi <= 200:
        return "Unhealthy (रातो)"
    elif aqi <= 300:
        return "Very Unhealthy (जम्मको रातो)"
    else:
        return "Hazardous (कालो)"

df['Category'] = df['AQI'].apply(get_aqi_category)
print(df[['Date', 'AQI', 'Category']])

# 2. कति दिन कौन category मा थे?
print("\n=== Category Distribution ===")
category_counts = df['Category'].value_counts()
print(category_counts)

# 3. PM2.5 vs PM10 comparison
print("\n=== Pollutants Comparison ===")
print(f"Average PM2.5: {df['PM25'].mean():.2f}")
print(f"Average PM10: {df['PM10'].mean():.2f}")
print(f"Which is higher? {'PM10' if df['PM10'].mean() > df['PM25'].mean() else 'PM25'}")








# STEP 2: More Advanced Analysis


# ============================================
# Advanced Visualizations
# ============================================

# Graph 2: Pie Chart (Category distribution)
plt.figure(figsize=(10, 7))
category_counts.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'yellow', 'orange', 'red', 'darkred'])
plt.title('Air Quality Categories Distribution')
plt.ylabel('')
plt.tight_layout()
plt.savefig('../output/aqi_categories_pie.png', dpi=300)
plt.show()

# Graph 3: Bar Chart (Pollutants)
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# PM2.5 vs PM10
ax[0].bar(['PM2.5', 'PM10'], [df['PM25'].mean(), df['PM10'].mean()], color=['skyblue', 'coral'])
ax[0].set_ylabel('Concentration (µg/m³)')
ax[0].set_title('Average Pollutant Levels')
ax[0].grid(True, alpha=0.3)

# Temperature vs Humidity
ax[1].plot(df.index, df['Temperature'], marker='o', label='Temperature (°C)', color='red')
ax[1].plot(df.index, df['Humidity'], marker='s', label='Humidity (%)', color='blue')
ax[1].set_xlabel('Days')
ax[1].set_ylabel('Value')
ax[1].set_title('Temperature vs Humidity')
ax[1].legend()
ax[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../output/pollutants_comparison.png', dpi=300)
plt.show()

# Graph 4: Heatmap style (जो दिन खराब थे)
plt.figure(figsize=(12, 4))
colors = ['green' if aqi <= 100 else 'yellow' if aqi <= 150 else 'orange' if aqi <= 200 else 'red' 
          for aqi in df['AQI']]
plt.bar(df.index, df['AQI'], color=colors, alpha=0.7)
plt.xlabel('Days')
plt.ylabel('AQI Level')
plt.title('Daily AQI with Color Coding')
plt.axhline(y=100, color='yellow', linestyle='--', label='Moderate Threshold')
plt.axhline(y=150, color='orange', linestyle='--', label='Unhealthy Threshold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../output/aqi_color_coded.png', dpi=300)
plt.show()





# STEP 3: Moving Average & Trends




# ============================================
# MOVING AVERAGE (Smoothing for trends)
# ============================================

print("\n=== MOVING AVERAGE ANALYSIS ===")

# 3-day moving average
df['AQI_MA3'] = df['AQI'].rolling(window=3).mean()

# 7-day moving average
df['AQI_MA7'] = df['AQI'].rolling(window=7).mean()

print("Moving averages calculated!")
print(df[['Date', 'AQI', 'AQI_MA3', 'AQI_MA7']])

# Visualization
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['AQI'], marker='o', label='Actual AQI', linewidth=2)
plt.plot(df.index, df['AQI_MA3'], label='3-day Average', linestyle='--', linewidth=2)
plt.plot(df.index, df['AQI_MA7'], label='7-day Average', linestyle='--', linewidth=2)
plt.xlabel('Days')
plt.ylabel('AQI')
plt.title('AQI with Moving Averages')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../output/moving_average.png', dpi=300)
plt.show()

# ============================================
# TREND DETECTION
# ============================================

# AQI improve भइरहेको छ कि खराब हुँदै छ?
first_half_avg = df['AQI'].iloc[:5].mean()
second_half_avg = df['AQI'].iloc[5:].mean()

print(f"\nPehilo आधा को average AQI: {first_half_avg:.2f}")
print(f"दोस्रो आधा को average AQI: {second_half_avg:.2f}")

if second_half_avg < first_half_avg:
    print("✓ अच्छी खबर! AQI improve हुँदै छ (घट्दै छ)")
else:
    print("⚠️ चिन्ता को कुरा! AQI खराब हुँदै छ (बढ्दै छ)")







# STEP 4: Simple Prediction 


    # ============================================
# SIMPLE LINEAR PREDICTION
# ============================================

print("\n=== FUTURE AQI PREDICTION ===")

# NumPy से linear fit
X = np.arange(len(df))
y = np.array(df['AQI'])

# Linear polynomial fit (straight line)
coefficients = np.polyfit(X, y, 1)
polynomial = np.poly1d(coefficients)

print(f"Trend line equation: AQI = {coefficients[0]:.4f} * day + {coefficients[1]:.4f}")

# अगिले 5 दिनको prediction
future_X = np.arange(len(df), len(df) + 5)
predicted_aqi = polynomial(future_X)

print("\nअगिले 5 दिनको AQI prediction:")
for i, pred in enumerate(predicted_aqi, 1):
    day_num = len(df) + i
    print(f"Day {day_num}: {pred:.1f}")

# Visualization
plt.figure(figsize=(12, 6))
plt.plot(X, y, marker='o', label='Actual AQI', linewidth=2, color='blue')
plt.plot(future_X, predicted_aqi, marker='o', label='Predicted AQI', linestyle='--', linewidth=2, color='red')
plt.axvline(x=len(df)-0.5, color='gray', linestyle=':', alpha=0.5)
plt.text(len(df)-1, max(y), 'Future', fontsize=10)
plt.xlabel('Days')
plt.ylabel('AQI')
plt.title('AQI Trend & Future Prediction')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../output/aqi_prediction.png', dpi=300)
plt.show()