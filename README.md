# Google Trends and Sustainable Mobility

This project analyzes Google Trends search data to explore urban mobility patterns from a sustainability perspective. We use Python and the `trendspy` library to extract, process, and analyze search trends related to different transportation modes.

## 📂 Project Structure
- `data/`: Raw and processed datasets from Google Trends.
- `scripts/`: Python scripts for data extraction and analysis.
- `notebooks/`: Jupyter notebooks for data exploration and visualization.
- `results/`: Graphs and final outputs of the analysis.
- `README.md`: Project overview and objectives.
- `.gitignore`: Files to exclude from version control.

## 🚀 Steps
1. **Build the base script** (`trendspy_scrape.py`):  
   - Extracts Google Trends data **one keyword at a time**.
   
2. **Extend the script for multiple keywords with a control term** (`trendspy_scrape_multiple_kw.py`):  
   - Uses a **control term** to ensure comparability across multiple queries.
   - Extracts data for multiple keywords at once while maintaining a consistent scale.

3. **Analyze and visualize trends**:  
   - Process the extracted data.
   - Normalize values using the control term.
   - Generate visualizations to identify mobility patterns.
