# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# ----------------------------
# Step 1: Load the data
# ----------------------------
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers using the CORD-19 metadata dataset.")

# Load CSV - use your unzipped file
CSV_PATH = 'metadata.csv'
df = pd.read_csv(CSV_PATH)

# ----------------------------
# Step 2: Basic Cleaning
# ----------------------------
# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Extract publication year
df['year'] = df['publish_time'].dt.year

# Create abstract word count
df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))

# Cleaned data: remove rows missing key info
df_clean = df.dropna(subset=['title', 'publish_time'])

# ----------------------------
# Step 3: Sidebar filters
# ----------------------------
st.sidebar.header("Filters")

# Year range slider
min_year = int(df_clean['year'].min())
max_year = int(df_clean['year'].max())
year_range = st.sidebar.slider("Select publication year range", min_year, max_year, (2020, 2021))

# Journal filter
top_journals = df_clean['journal'].value_counts().head(20).index.tolist()
journal_selected = st.sidebar.multiselect("Select journals", top_journals, top_journals)

# Apply filters
filtered = df_clean[
    (df_clean['year'] >= year_range[0]) &
    (df_clean['year'] <= year_range[1]) &
    (df_clean['journal'].isin(journal_selected))
]

st.write(f"Showing {len(filtered)} papers after filtering")

# ----------------------------
# Step 4: Data display
# ----------------------------
st.subheader("Sample of Papers")
st.dataframe(filtered[['title', 'authors', 'journal', 'year']].head(20))

# ----------------------------
# Step 5: Visualizations
# ----------------------------
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
ax.set_title('Publications by Year')
st.pyplot(fig)

st.subheader("Top Journals")
journal_counts = filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
ax2.bar(journal_counts.index, journal_counts.values)
ax2.set_ylabel('Number of Papers')
ax2.set_title('Top Journals Publishing COVID-19 Research')
plt.xticks(rotation=45)
st.pyplot(fig2)

st.subheader("Most Frequent Words in Titles")
# Word frequency
all_titles = ' '.join(filtered['title'].dropna()).lower()
words = re.findall(r'\b\w+\b', all_titles)
word_counts = Counter(words)
common_words = word_counts.most_common(20)

words_list, counts_list = zip(*common_words)
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.bar(words_list, counts_list)
plt.xticks(rotation=45)
ax3.set_ylabel('Frequency')
ax3.set_title('Top 20 Words in Paper Titles')
st.pyplot(fig3)

# Optional: show distribution by source_x
if 'source_x' in df_clean.columns:
    st.subheader("Papers by Source")
    source_counts = filtered['source_x'].value_counts().head(10)
    fig4, ax4 = plt.subplots()
    ax4.bar(source_counts.index, source_counts.values)
    ax4.set_ylabel('Number of Papers')
    ax4.set_title('Top Sources of Papers')
    plt.xticks(rotation=45)
    st.pyplot(fig4)

# ----------------------------
# Step 6: Summary Statistics
# ----------------------------
st.subheader("Summary Statistics")
st.write("Basic numeric stats")
st.write(filtered.describe())

st.write("Missing values per column")
st.write(filtered.isnull().sum())

st.write("Columns in the dataset")
st.write(filtered.columns.tolist())

st.write("Data dimensions")
st.write(f"Rows: {filtered.shape[0]}, Columns: {filtered.shape[1]}")
