# TED Talks Exploratory Data Analysis (EDA)

Exploratory Data Analysis on the **TED - Ultimate Dataset** from Kaggle ([miguelcorraljr/ted-ultimate-dataset](https://www.kaggle.com/datasets/miguelcorraljr/ted-ultimate-dataset)).

---

## 📌 Overview
This repository contains a complete Exploratory Data Analysis (EDA) of TED Talks metadata and transcripts. The goal of this analysis is to understand viewership dynamics, speaker distributions, talk duration patterns, language availability, speaking rates (WPM), and key themes that characterize popular TED talks.

---

## 📂 Project Structure
```text
├── data/
│   └── ted_talks_en.csv             # Cleaned English TED talks dataset
├── images/                          # High-resolution exported EDA charts
│   ├── 01_top_10_most_viewed_talks.png
│   ├── 02_top_speakers_by_views.png
│   ├── 03_top_speakers_by_talks.png
│   ├── 04_views_distribution.png
│   ├── 05_duration_distribution.png
│   ├── 06_comments_vs_views.png
│   ├── 07_talks_per_year.png
│   ├── 08_avg_views_per_year.png
│   ├── 09_day_of_week_distribution.png
│   ├── 10_top_20_topics.png
│   ├── 11_topics_wordcloud.png
│   ├── 12_speaking_rate_distribution.png
│   ├── 13_correlation_heatmap.png
│   ├── 14_most_debated_talks.png
│   └── 15_available_languages_distribution.png
├── ted_talks_eda.ipynb              # Executed Jupyter Notebook with all outputs & plots
├── eda_analysis.py                  # Python script to reproduce full analysis and plots
├── requirements.txt                 # Dependencies
└── README.md                        # Documentation & insights
```

---

## ⚙️ Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Python Script
```bash
python eda_analysis.py
```

### 3. Or Open the Jupyter Notebook
```bash
jupyter notebook ted_talks_eda.ipynb
```

---

## 📊 Key Highlights & Findings

1. **Viewership Distribution:**
   - Views follow a heavily right-skewed Pareto distribution.
   - The median views per talk is **~1.37 Million**, while viral outliers exceed **40–65 Million** (e.g., Sir Ken Robinson's *"Do schools kill creativity?"* and Amy Cuddy's *"Your body language may shape who you are"*).

2. **Duration & The 18-Minute Rule:**
   - Talk durations strictly concentrate around **12 to 18 minutes** (median = 12.3 mins), aligning with TED's signature talk format limit.
   - A smaller secondary spike occurs around **3–5 minutes** representing short animations and TED-Ed lessons.

3. **Speaking Pace (WPM):**
   - Transcripts combined with duration show a mean speaking pace of **~147.4 Words Per Minute (WPM)**, fitting conversational English standards (~140–160 WPM).

4. **Publishing Trends:**
   - Talk releases heavily peak on weekdays—specifically **Tuesday, Wednesday, and Thursday**. Weekend uploads are virtually non-existent.

5. **Global Accessibility & Languages:**
   - Talks have a median of **25 available subtitle languages**.
   - Available languages correlate positively ($r \approx 0.38$) with total views, underscoring the role of international localization in audience reach.

6. **Primary Themes:**
   - The most recurring topic tags are **Science, Technology, Culture, Global Issues, Design, and Business**.

---
*Created as part of the internship curriculum.*
