# CORD-19 Data Explorer

A simple **Streamlit app** to explore COVID-19 research papers using the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge).

This app allows you to:
- Filter papers by publication year and top journals
- View a sample of research papers
- Analyze publication trends over time
- Explore the most frequent words in paper titles
- Visualize top journals and sources

---

## Features

- **Interactive sidebar filters** for year and journals
- **Data visualizations**:
  - Publications per year
  - Top journals publishing COVID-19 research
  - Most frequent words in paper titles
  - Distribution by source
- **Summary statistics** and missing values overview
- **Data preview** (sample of papers)

---

## Requirements

- Python 3.10+  
- Streamlit  
- Pandas  
- Matplotlib  

You can install the required packages with:

```bash
pip install streamlit pandas matplotlib
