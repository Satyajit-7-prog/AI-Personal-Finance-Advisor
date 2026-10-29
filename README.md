# AI Personal Finance Advisor

An AI-powered personal finance application built with Python, Machine Learning, and Streamlit to help users understand their financial health and explore spending insights.

## Overview

The AI Personal Finance Advisor is a machine-learning-based project designed to analyze financial information and provide users with insights into their financial situation.

The project includes a Streamlit web application, a financial analysis module, trained machine-learning artifacts, and a Jupyter notebook for model development.

## Features

- Interactive web interface built with Streamlit
- Financial analysis through a dedicated Python module
- Machine-learning model for financial health analysis
- Saved model and preprocessing artifacts
- Jupyter notebook for model development
- CSV datasets for training and analysis

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Structure

```text
AI-Personal-Finance-Advisor/
├── adviser/
│   └── financial_advisor.py
├── data/
│   ├── Indian_Personal_FinanceandSpending_Habits_data.csv
│   └── synthetic_personal_finance_dataset.csv
├── saved_model/
│   ├── financial_health_model.pkl
│   └── financial_health_preprocessor.pkl
├── Finance_model.ipynb
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Satyajit-7-prog/AI-Personal-Finance-Advisor.git
cd AI-Personal-Finance-Advisor
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python -m streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser.

## Model Development

The `Finance_model.ipynb` notebook contains the model-development workflow. The trained model and preprocessing artifacts used by the application are stored in `saved_model/`.

## Datasets

The `data/` directory contains the CSV datasets used in this project. Check the original dataset sources and licenses before redistributing or reusing them.

## Future Improvements

- Improve financial insights and recommendations
- Add interactive visualizations and spending summaries
- Improve model evaluation and validation
- Add input validation and error handling
- Deploy the application online

## Disclaimer

This project is for educational and informational purposes only. It does not provide professional financial, investment, tax, or legal advice. Independently verify important financial decisions.

GitHub: [Satyajit-7-prog](https://github.com/Satyajit-7-prog)