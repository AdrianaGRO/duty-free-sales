# Duty Free Sales Analyzer 📊
This is my first AI-powered project that analyzes sales from a duty-free shop.
It loads Excel Data, performs calculations and generate a smart summary using OpenAI GPT.
Initially build in Google Colab, I switched to VS Code for Day 6 Streamlit dashboard due to Colabs's Streamlit compability issues.

## Features 🚀

- Loads and processes Excel sales data;
- Calculate revenue and margin by category;
- Identifies top-3-selling and most profiatble products
- Analyzes daily sales trends (March 1 - April 30, 2025)
- Integrates promo data for actionable insights
- Generates an AI business summary using GPT-3.5
- Uses mock external trends (eg. Children's Day on 1 June, Chocolate and Toys Boost) for predictions
- Predicts a sale spike for Chidren's Day with chocolate and toys promo
  

### How to use 🛠️

1. Clone the repository.
2. Make sure your OpenAI key is saved in secret environment ("OPEN_AI")
3. Run the Streamlit dashboard with the command in the terminal: streamlit run app.py
4. View at : http://localhost:8501/ the dashboard.

#### Files 📂

- **Notebooks:** DutyFreeSalesAnalyzer_Day2.ipynb, DutyFreeSalesAnalyzer_Day3.ipynb, DutyFreeSalesAnalyzer_Day4.ipynb, DutyFreeSalesAnalyzer_Day5.ipynb
- **Day 6 App:** app.py (Streamlit dashboard)
- **Data:** duty_free_sales.xlsx (31,264 units), duty_free_sales_day3.xlsx, promo.csv
- **Outputs:** sales_summary_day2.txt, sales_summary_day3.txt, sales_summary_day4.txt, sales_summary_day5.txt, trends_plot.png, trends_plot_day4.png, trends_plot_day5.png

##### Author

👩‍💻 Created by Adriana PyArch

