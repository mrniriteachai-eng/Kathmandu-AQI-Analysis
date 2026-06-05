"""
Kathmandu Air Quality Analysis
सब कुरा एकै जठ्ठा
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===== DATA LOADING =====
print("📊 Data load गरिँदै...")
df = pd.read_csv('../data/kathmandu_aqi.csv')
print(f"✓ {len(df)} days का data loaded!")

# ===== BASIC STATISTICS =====
print("\n" + "="*50)
print("KATHMANDU AIR QUALITY SUMMARY")
print("="*50)

aqi_stats = {
    'Average AQI': f"{df['AQI'].mean():.1f}",
    'Highest AQI': f"{df['AQI'].max()}",
    'Lowest AQI': f"{df['AQI'].min()}",
    'Std Deviation': f"{df['AQI'].std():.1f}",
}

for key, value in aqi_stats.items():
    print(f"{key}: {value}")

# ===== CATEGORY ANALYSIS =====
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy (Sensitive)"
    elif aqi <= 200:
        return "Unhealthy"
    else:
        return "Very Unhealthy"

df['Category'] = df['AQI'].apply(get_aqi_category)

print("\n📍 Category Distribution:")
print(df['Category'].value_counts())

# ===== POLLUTANTS ANALYSIS =====
print("\n💨 Pollutant Levels:")
print(f"PM2.5 Average: {df['PM25'].mean():.1f} µg/m³")
print(f"PM10 Average: {df['PM10'].mean():.1f} µg/m³")
print(f"NO2 Average: {df['NO2'].mean():.1f} ppb")

# ===== MOVING AVERAGES =====
df['MA3'] = df['AQI'].rolling(window=3).mean()
df['MA7'] = df['AQI'].rolling(window=7).mean()

# ===== PREDICTION =====
X = np.arange(len(df))
y = np.array(df['AQI'])
coef = np.polyfit(X, y, 1)
poly = np.poly1d(coef)

future_X = np.arange(len(df), len(df) + 5)
predictions = poly(future_X)

print("\n🔮 अगिले 5 दिनको AQI prediction:")
for i, pred in enumerate(predictions, 1):
    print(f"   Day {len(df)+i}: {pred:.1f}")

# ===== VISUALIZATIONS =====
print("\n📈 Graphs बनाइँदै...")

fig = plt.figure(figsize=(16, 12))

# Plot 1: Main AQI Trend
ax1 = plt.subplot(3, 2, 1)
ax1.plot(df.index, df['AQI'], marker='o', color='red', linewidth=2, label='Actual')
ax1.fill_between(df.index, df['AQI'], alpha=0.3, color='red')
ax1.set_title('Daily AQI Levels', fontsize=12, fontweight='bold')
ax1.set_xlabel('Days')
ax1.set_ylabel('AQI')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Plot 2: Moving Averages
ax2 = plt.subplot(3, 2, 2)
ax2.plot(df.index, df['AQI'], marker='o', label='Actual', alpha=0.5)
ax2.plot(df.index, df['MA3'], label='3-day MA', linestyle='--')
ax2.plot(df.index, df['MA7'], label='7-day MA', linestyle='--')
ax2.set_title('AQI with Moving Averages', fontsize=12, fontweight='bold')
ax2.set_xlabel('Days')
ax2.set_ylabel('AQI')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Plot 3: Category Pie Chart
ax3 = plt.subplot(3, 2, 3)
category_counts = df['Category'].value_counts()
ax3.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
ax3.set_title('Air Quality Categories', fontsize=12, fontweight='bold')

# Plot 4: Pollutants Bar Chart
ax4 = plt.subplot(3, 2, 4)
pollutants = ['PM2.5', 'PM10', 'NO2']
values = [df['PM25'].mean(), df['PM10'].mean(), df['NO2'].mean()]
ax4.bar(pollutants, values, color=['skyblue', 'coral', 'lightgreen'])
ax4.set_title('Average Pollutant Levels', fontsize=12, fontweight='bold')
ax4.set_ylabel('Concentration')
ax4.grid(True, alpha=0.3, axis='y')

# Plot 5: Color-coded Bar Chart
ax5 = plt.subplot(3, 2, 5)
colors = ['green' if aqi <= 100 else 'yellow' if aqi <= 150 else 'red' for aqi in df['AQI']]
ax5.bar(df.index, df['AQI'], color=colors, alpha=0.7)
ax5.axhline(y=100, color='yellow', linestyle='--', alpha=0.5, label='Moderate')
ax5.axhline(y=150, color='red', linestyle='--', alpha=0.5, label='Unhealthy')
ax5.set_title('Daily AQI (Color Coded)', fontsize=12, fontweight='bold')
ax5.set_xlabel('Days')
ax5.set_ylabel('AQI')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# Plot 6: Prediction
ax6 = plt.subplot(3, 2, 6)
ax6.plot(X, y, marker='o', label='Actual', linewidth=2)
ax6.plot(future_X, predictions, marker='o', label='Predicted', linestyle='--', color='red', linewidth=2)
ax6.axvline(x=len(df)-0.5, color='gray', linestyle=':', alpha=0.5)
ax6.set_title('AQI Prediction (Next 5 Days)', fontsize=12, fontweight='bold')
ax6.set_xlabel('Days')
ax6.set_ylabel('AQI')
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../output/complete_analysis.png', dpi=300, bbox_inches='tight')
print("✓ सब graphs saved!")
plt.show()

# ===== FINAL INSIGHTS =====
print("\n" + "="*50)
print("📋 FINAL INSIGHTS & RECOMMENDATIONS")
print("="*50)

avg_aqi = df['AQI'].mean()
if avg_aqi <= 50:
    status = "✓ Good - बाहिर खेल्न सकिन्छ"
elif avg_aqi <= 100:
    status = "✓ Moderate - सामान्य स्वस्थ मानिसको लागि ठीक"
elif avg_aqi <= 150:
    status = "⚠️ Unhealthy - संवेदनशील मानिसहरु सावधान रहुन्"
else:
    status = "🚨 Very Unhealthy - सबै मानिस बाहिर निस्कन सक्दैन"

print(f"\nAverage Status: {status}")

# Trend
first_half = df['AQI'].iloc[:len(df)//2].mean()
second_half = df['AQI'].iloc[len(df)//2:].mean()

if second_half < first_half:
    trend = "📈 improving"
else:
    trend = "📉 worsening"

print(f"Trend: Air quality {trend}")

print("\n✓ Analysis Complete!")