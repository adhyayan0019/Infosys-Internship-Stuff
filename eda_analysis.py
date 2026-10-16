import os
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import warnings

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 150

os.makedirs('images', exist_ok=True)

# load data
df = pd.read_csv('data/ted_talks_en.csv')
print(f"Dataset shape: {df.shape}")

# missing values
null_counts = df.isnull().sum()
print("\nMissing values:\n", null_counts[null_counts > 0])

# date features
df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
df['recorded_date'] = pd.to_datetime(df['recorded_date'], errors='coerce')
df['published_year'] = df['published_date'].dt.year
df['published_month'] = df['published_date'].dt.month
df['published_day_name'] = df['published_date'].dt.day_name()

# duration in minutes
df['duration_min'] = df['duration'] / 60.0

# parse list columns
def parse_list(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return []
    return []

df['topics_list'] = df['topics'].apply(parse_list)
df['available_lang_list'] = df['available_lang'].apply(parse_list)

df['num_topics'] = df['topics_list'].apply(len)
df['num_languages'] = df['available_lang_list'].apply(len)

# text stats
df['transcript_word_count'] = df['transcript'].fillna('').apply(lambda x: len(str(x).split()))
df['speaking_rate_wpm'] = df['transcript_word_count'] / df['duration_min']
# filter absurd wpm values (e.g. musical performances or silent talks)
df['speaking_rate_wpm'] = df['speaking_rate_wpm'].replace([np.inf, -np.inf], np.nan)

# engagement metrics
df['comments_per_1k_views'] = (df['comments'] / df['views']) * 1000

print("\nSummary Statistics of Numeric Features:")
print(df[['views', 'comments', 'duration_min', 'num_languages', 'speaking_rate_wpm']].describe())

# 1. Top 10 Most Viewed Talks
top10_views = df.sort_values(by='views', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=top10_views, x='views', y='title', palette='magma')
plt.title('Top 10 Most Viewed TED Talks', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Total Views (in Tens of Millions)', fontsize=11)
plt.ylabel('Talk Title', fontsize=11)
plt.tight_layout()
plt.savefig('images/01_top_10_most_viewed_talks.png')
plt.close()

# 2. Top 10 Speakers by Total Views
top_speakers_views = df.groupby('speaker_1')['views'].sum().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(data=top_speakers_views, x='views', y='speaker_1', palette='viridis')
plt.title('Top 10 Speakers by Total Views', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Total Cumulative Views', fontsize=11)
plt.ylabel('Speaker', fontsize=11)
plt.tight_layout()
plt.savefig('images/02_top_speakers_by_views.png')
plt.close()

# 3. Top 10 Speakers by Number of Talks
top_speakers_talks = df['speaker_1'].value_counts().head(10).reset_index()
top_speakers_talks.columns = ['speaker_1', 'talk_count']
plt.figure(figsize=(10, 5))
sns.barplot(data=top_speakers_talks, x='talk_count', y='speaker_1', palette='crest')
plt.title('Top 10 Speakers with Most TED Talks', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Number of Talks', fontsize=11)
plt.ylabel('Speaker', fontsize=11)
plt.tight_layout()
plt.savefig('images/03_top_speakers_by_talks.png')
plt.close()

# 4. Distribution of Views (Log scale)
plt.figure(figsize=(9, 5))
sns.histplot(df['views'], bins=50, kde=True, color='#1f77b4', log_scale=True)
plt.title('Distribution of Talk Views (Log Scale)', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Views (Log Scale)', fontsize=11)
plt.ylabel('Number of Talks', fontsize=11)
plt.tight_layout()
plt.savefig('images/04_views_distribution.png')
plt.close()

# 5. Distribution of Duration
plt.figure(figsize=(9, 5))
sns.histplot(df['duration_min'], bins=40, kde=True, color='#ff7f0e')
plt.axvline(df['duration_min'].median(), color='red', linestyle='--', label=f'Median ({df["duration_min"].median():.1f} min)')
plt.axvline(18, color='green', linestyle=':', label='18 min TED Limit')
plt.title('Distribution of Talk Duration in Minutes', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Duration (Minutes)', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig('images/05_duration_distribution.png')
plt.close()

# 6. Comments vs Views
plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x='views', y='comments', alpha=0.5, color='#2ca02c')
plt.xscale('log')
plt.yscale('log')
plt.title('Relationship between Views and Comments (Log-Log Scale)', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Views (Log Scale)', fontsize=11)
plt.ylabel('Comments (Log Scale)', fontsize=11)
plt.tight_layout()
plt.savefig('images/06_comments_vs_views.png')
plt.close()

# 7. Talks per Year Trend
yearly = df['published_year'].value_counts().sort_index()
# remove incomplete current year if needed or plot all
plt.figure(figsize=(10, 5))
sns.lineplot(x=yearly.index, y=yearly.values, marker='o', color='#d62728', linewidth=2.5)
plt.title('Growth of TED Talks Over Years (Published)', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Year', fontsize=11)
plt.ylabel('Number of Talks Published', fontsize=11)
plt.xticks(yearly.index, rotation=45)
plt.tight_layout()
plt.savefig('images/07_talks_per_year.png')
plt.close()

# 8. Average Views per Year
avg_views_year = df.groupby('published_year')['views'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(data=avg_views_year, x='published_year', y='views', palette='coolwarm')
plt.title('Average Views per Talk by Publication Year', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Year', fontsize=11)
plt.ylabel('Average Views', fontsize=11)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/08_avg_views_per_year.png')
plt.close()

# 9. Day of Week Distribution
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = df['published_day_name'].value_counts().reindex(day_order)
plt.figure(figsize=(9, 5))
sns.barplot(x=day_counts.index, y=day_counts.values, palette='Blues_d')
plt.title('TED Talks Published by Day of the Week', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Day of Week', fontsize=11)
plt.ylabel('Number of Talks', fontsize=11)
plt.tight_layout()
plt.savefig('images/09_day_of_week_distribution.png')
plt.close()

# 10. Top 20 Topics Frequency
all_topics = [t for sublist in df['topics_list'] for t in sublist]
topics_series = pd.Series(all_topics).value_counts().head(20)
plt.figure(figsize=(10, 7))
sns.barplot(x=topics_series.values, y=topics_series.index, palette='mako')
plt.title('Top 20 Most Frequent Topics in TED Talks', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Frequency', fontsize=11)
plt.ylabel('Topic Tag', fontsize=11)
plt.tight_layout()
plt.savefig('images/10_top_20_topics.png')
plt.close()

# 11. Word Cloud of Topics
text_topics = " ".join([t.replace(' ', '_') for t in all_topics])
wc = WordCloud(width=1000, height=500, background_color='white', colormap='tab10').generate(text_topics)
plt.figure(figsize=(12, 6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of TED Talk Topics', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('images/11_topics_wordcloud.png')
plt.close()

# 12. Speaking Rate (Words Per Minute) Distribution
valid_wpm = df[(df['speaking_rate_wpm'] >= 60) & (df['speaking_rate_wpm'] <= 260)]['speaking_rate_wpm']
plt.figure(figsize=(9, 5))
sns.histplot(valid_wpm, bins=35, kde=True, color='#9467bd')
plt.axvline(valid_wpm.mean(), color='red', linestyle='--', label=f'Average WPM ({valid_wpm.mean():.1f})')
plt.title('Distribution of Speaking Rate (Words Per Minute)', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Words Per Minute (WPM)', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig('images/12_speaking_rate_distribution.png')
plt.close()

# 13. Correlation Heatmap
corr_cols = ['views', 'comments', 'duration_min', 'num_languages', 'num_topics', 'transcript_word_count', 'speaking_rate_wpm']
corr_matrix = df[corr_cols].corr()
plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True, linewidths=0.5)
plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('images/13_correlation_heatmap.png')
plt.close()

# 14. Top 10 Most Debated Talks (Comments per 1k views)
debated = df[df['views'] > 100000].sort_values(by='comments_per_1k_views', ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(data=debated, x='comments_per_1k_views', y='title', palette='flare')
plt.title('Top 10 Most Debated Talks (Comments per 1,000 Views)', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Comments per 1,000 Views', fontsize=11)
plt.ylabel('Talk Title', fontsize=11)
plt.tight_layout()
plt.savefig('images/14_most_debated_talks.png')
plt.close()

# 15. Available Languages Distribution
plt.figure(figsize=(9, 5))
sns.histplot(df['num_languages'], bins=30, kde=True, color='#17becf')
plt.axvline(df['num_languages'].median(), color='red', linestyle='--', label=f'Median ({df["num_languages"].median():.0f} langs)')
plt.title('Distribution of Subtitle Languages per Talk', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Number of Available Languages', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig('images/15_available_languages_distribution.png')
plt.close()

print("\nAll 15 visualizations generated and saved to images/ successfully!")
