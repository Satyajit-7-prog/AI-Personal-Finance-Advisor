import pandas as pd
import joblib
import os


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "saved_model"
)


MODEL_PATH = os.path.join(
    MODEL_DIR,
    "financial_health_model.pkl"
)


PREPROCESSOR_PATH = os.path.join(
    MODEL_DIR,
    "financial_health_preprocessor.pkl"
)


# ============================================================
# CHECK MODEL FILES
# ============================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Financial health model not found at:\n{MODEL_PATH}"
    )

if not os.path.exists(PREPROCESSOR_PATH):
    raise FileNotFoundError(
        f"Financial health preprocessor not found at:\n"
        f"{PREPROCESSOR_PATH}"
    )


# ============================================================
# LOAD SAVED MODEL
# ============================================================

financial_health_model = joblib.load(
    MODEL_PATH
)


# ============================================================
# LOAD SAVED PREPROCESSOR
# ============================================================

financial_health_preprocessor = joblib.load(
    PREPROCESSOR_PATH
)


# ============================================================
# EXPENSE COLUMNS
# ============================================================

EXPENSE_COLUMNS = [
    "Rent",
    "Loan_Repayment",
    "Insurance",
    "Groceries",
    "Transport",
    "Eating_Out",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Education",
    "Miscellaneous"
]


# ============================================================
# EXPENSE THRESHOLDS
# ============================================================
# These thresholds are taken from the corrected Finance_model.ipynb.
# Values are expense percentages of income, based on the dataset's
# 25th percentile, median (50th percentile), 75th percentile, and
# 90th percentile, respectively.

EXPENSE_THRESHOLDS = {
    "Rent": {
        "very_low": 20.00,
        "low": 20.00,
        "moderate": 30.00,
        "high": 30.00,
    },
    "Loan_Repayment": {
        "very_low": 0.00,
        "low": 0.00,
        "moderate": 10.63,
        "high": 16.29,
    },
    "Insurance": {
        "very_low": 2.74,
        "low": 3.49,
        "moderate": 4.24,
        "high": 4.70,
    },
    "Groceries": {
        "very_low": 11.27,
        "low": 12.54,
        "moderate": 13.78,
        "high": 14.51,
    },
    "Transport": {
        "very_low": 5.76,
        "low": 6.50,
        "moderate": 7.24,
        "high": 7.70,
    },
    "Eating_Out": {
        "very_low": 2.76,
        "low": 3.51,
        "moderate": 4.25,
        "high": 4.70,
    },
    "Entertainment": {
        "very_low": 2.73,
        "low": 3.49,
        "moderate": 4.25,
        "high": 4.69,
    },
    "Utilities": {
        "very_low": 5.01,
        "low": 6.02,
        "moderate": 7.01,
        "high": 7.62,
    },
    "Healthcare": {
        "very_low": 3.50,
        "low": 3.99,
        "moderate": 4.49,
        "high": 4.80,
    },
    "Education": {
        "very_low": 5.31,
        "low": 6.91,
        "moderate": 8.43,
        "high": 9.39,
    },
    "Miscellaneous": {
        "very_low": 1.51,
        "low": 2.01,
        "moderate": 2.51,
        "high": 2.80,
    },
}


# ============================================================
# MAIN FINANCIAL ANALYSIS FUNCTION
# ============================================================

def analyze_user_finances(
    income,
    age,
    dependents,
    city_tier,
    rent,
    loan_repayment,
    insurance,
    groceries,
    transport,
    eating_out,
    entertainment,
    utilities,
    healthcare,
    education,
    miscellaneous,
    desired_savings
):

    if income <= 0:
        raise ValueError("Income must be greater than zero.")

    # ========================================================
    # 1. CREATE USER DATAFRAME
    # ========================================================

    user = pd.DataFrame([{

        "Income": income,

        "Age": age,

        "Dependents": dependents,

        "City_Tier": city_tier,

        "Rent": rent,

        "Loan_Repayment": loan_repayment,

        "Insurance": insurance,

        "Groceries": groceries,

        "Transport": transport,

        "Eating_Out": eating_out,

        "Entertainment": entertainment,

        "Utilities": utilities,

        "Healthcare": healthcare,

        "Education": education,

        "Miscellaneous": miscellaneous,

        "Desired_Savings": desired_savings

    }])


    # ========================================================
    # 2. TOTAL EXPENSES
    # ========================================================

    user["Total_Expenses"] = (
        user[EXPENSE_COLUMNS].sum(axis=1)
    )


    # ========================================================
    # 3. EXPENSE RATIOS
    # ========================================================

    for category in EXPENSE_COLUMNS:

        ratio_column = (
            category + "_Ratio"
        )

        user[ratio_column] = (
            user[category]
            /
            user["Income"]
        )


    # ========================================================
    # 4. EXPENSE STATUS (FIVE LEVELS)
    # ========================================================

    for category in EXPENSE_COLUMNS:

        ratio_column = category + "_Ratio"
        status_column = category + "_Status"
        percentage = user[ratio_column] * 100

        thresholds = EXPENSE_THRESHOLDS[category]

        very_low_threshold = thresholds["very_low"]
        low_threshold = thresholds["low"]
        moderate_threshold = thresholds["moderate"]
        high_threshold = thresholds["high"]

        # Apply percentile thresholds in ascending order, as in the notebook.
        user[status_column] = "Very Low"

        user.loc[
            percentage >= very_low_threshold,
            status_column
        ] = "Low"

        user.loc[
            percentage >= low_threshold,
            status_column
        ] = "Moderate"

        user.loc[
            percentage >= moderate_threshold,
            status_column
        ] = "High"

        user.loc[
            percentage >= high_threshold,
            status_column
        ] = "Very High"

        # Preserve the notebook's rule: zero or negative spending is Very Low,
        # including categories where one or more percentiles equal zero.
        user.loc[
            percentage <= 0,
            status_column
        ] = "Very Low"


    # ========================================================
    # 5. EXPENSE RECOMMENDATIONS
    # ========================================================

    expense_recommendations = []

    for category in EXPENSE_COLUMNS:

        status_column = category + "_Status"
        status = user[status_column].iloc[0]
        category_name = category.replace("_", " ").lower()

        if status == "Very High":
            expense_recommendations.append(
                f"High priority: Review your {category_name} spending "
                "because it is relatively very high."
            )

        elif status == "High":
            expense_recommendations.append(
                f"Consider reviewing your {category_name} spending "
                "because it is relatively high."
            )

        elif status == "Moderate":
            expense_recommendations.append(
                f"Monitor your {category_name} spending and look for "
                "opportunities to save."
            )

        elif status == "Low":
            expense_recommendations.append(
                f"Your {category_name} spending is relatively low "
                "compared with the dataset."
            )

        else:  # Very Low
            expense_recommendations.append(
                f"Your {category_name} spending is very low compared "
                "with the dataset. Check that essential needs are "
                "still being covered."
            )

    user["Expense_Recommendations"] = [
        expense_recommendations
    ]


    # ========================================================
    # 6. REMAINING INCOME
    # ========================================================

    user["Remaining_Income"] = (
        user["Income"]
        -
        user["Total_Expenses"]
    )


    # ========================================================
    # 7. SAVINGS FEASIBILITY
    # ========================================================

    user["Savings_Feasibility"] = (
        user["Remaining_Income"]
        -
        user["Desired_Savings"]
    )


    # ========================================================
    # 8. SAVINGS BUFFER PERCENTAGE
    # ========================================================

    user["Savings_Buffer_Percentage"] = (

        user["Savings_Feasibility"]
        /
        user["Income"]
        *
        100

    )


    # ========================================================
    # 9. SAVINGS STATUS
    # ========================================================

    user["Savings_Status"] = (
        "Savings Goal Feasible"
    )

    user.loc[
        user["Savings_Feasibility"] < 0,
        "Savings_Status"
    ] = "Savings Goal Not Feasible"


    # ========================================================
    # 10. DETAILED SAVINGS STATUS
    # ========================================================

    user["Detailed_Savings_Status"] = (
        "Feasible - Low Buffer"
    )

    # Not feasible
    user.loc[
        user["Savings_Feasibility"] < 0,
        "Detailed_Savings_Status"
    ] = "Savings Goal Not Feasible"

    # Strong buffer
    user.loc[
        user["Savings_Buffer_Percentage"] >= 20,
        "Detailed_Savings_Status"
    ] = "Feasible - Strong Buffer"

    # Good buffer
    user.loc[
        (
            user["Savings_Buffer_Percentage"] >= 15
        )
        &
        (
            user["Savings_Buffer_Percentage"] < 20
        ),
        "Detailed_Savings_Status"
    ] = "Feasible - Good Buffer"

    # Moderate buffer
    user.loc[
        (
            user["Savings_Buffer_Percentage"] >= 8
        )
        &
        (
            user["Savings_Buffer_Percentage"] < 15
        ),
        "Detailed_Savings_Status"
    ] = "Feasible - Moderate Buffer"


    # ========================================================
    # 11. SAVINGS RECOMMENDATION
    # ========================================================

    savings_recommendations = []

    savings_buffer = (
        user[
            "Savings_Buffer_Percentage"
        ].iloc[0]
    )

    savings_feasibility = (
        user[
            "Savings_Feasibility"
        ].iloc[0]
    )


    if savings_feasibility < 0:

        savings_recommendations.append(
            "Your savings goal is not feasible "
            "with your current income and expenses. "
            "Consider reducing expenses or lowering "
            "your savings target."
        )

    elif savings_buffer < 8:

        savings_recommendations.append(
            "Your savings goal is feasible, but "
            "your remaining financial buffer is low. "
            "Monitor your expenses carefully."
        )

    elif savings_buffer < 15:

        savings_recommendations.append(
            "Your savings goal is feasible with a "
            "moderate financial buffer. Continue "
            "monitoring your expenses and savings."
        )

    elif savings_buffer < 20:

        savings_recommendations.append(
            "Your savings goal is feasible with a "
            "good financial buffer. Continue "
            "maintaining your current financial habits."
        )

    else:

        savings_recommendations.append(
            "Your savings goal is feasible with a "
            "strong financial buffer. You have "
            "good room for additional financial goals."
        )


    user[
        "Savings_Recommendation"
    ] = [
        savings_recommendations
    ]


    # ========================================================
    # 12. LOAN PAYMENT RATIO
    # ========================================================

    user["loan_payment_ratio"] = (
        user["Loan_Repayment"]
        /
        user["Income"]
    )


    # ========================================================
    # 13. DEBT STATUS
    # ========================================================

    user["Debt_Status"] = (
        "No Loan Repayment"
    )

    # Very high loan burden
    user.loc[
        user["loan_payment_ratio"] > 0.1628816388,
        "Debt_Status"
    ] = "Very High Loan Burden"

    # High loan burden
    user.loc[
        (
            user["loan_payment_ratio"] > 0.1063281034
        )
        &
        (
            user["loan_payment_ratio"] <= 0.1628816388
        ),
        "Debt_Status"
    ] = "High Loan Burden"

    # Normal loan burden
    user.loc[
        (
            user["loan_payment_ratio"] > 0
        )
        &
        (
            user["loan_payment_ratio"] <= 0.1063281034
        ),
        "Debt_Status"
    ] = "Normal Loan Burden"


    # ========================================================
    # 14. DEBT RECOMMENDATION
    # ========================================================

    debt_status = (
        user[
            "Debt_Status"
        ].iloc[0]
    )


    if debt_status == "No Loan Repayment":

        debt_recommendation = (
            "You currently have no loan repayment "
            "burden based on the provided information."
        )

    elif debt_status == "Normal Loan Burden":

        debt_recommendation = (
            "Your loan repayment is relatively "
            "moderate compared with the income "
            "distribution in the dataset. Continue "
            "monitoring your loan burden."
        )

    elif debt_status == "High Loan Burden":

        debt_recommendation = (
            "Your loan repayment takes a relatively "
            "high share of your income. Consider "
            "reducing debt or avoiding additional "
            "unnecessary borrowing."
        )

    else:

        debt_recommendation = (
            "Your loan repayment takes a very high "
            "share of your income. Consider prioritizing "
            "debt reduction and reviewing your expenses."
        )


    user[
        "Debt_Recommendation"
    ] = [
        debt_recommendation
    ]


    # ========================================================
    # 15. MACHINE LEARNING MODEL INPUT
    # ========================================================

    model_input = user[
        [
            "Age",
            "Dependents",
            "City_Tier",
            "Income",
            "Total_Expenses",
            "Loan_Repayment",
            "Desired_Savings"
        ]
    ]


    # ========================================================
    # 16. PREPROCESS MODEL INPUT
    # ========================================================

    encoded_input = (
        financial_health_preprocessor.transform(
            model_input
        )
    )


    # ========================================================
    # 17. FINANCIAL HEALTH PREDICTION
    # ========================================================

    financial_health = (
        financial_health_model.predict(
            encoded_input
        )
    )


    user[
        "Financial_Health"
    ] = financial_health[0]


    # ========================================================
    # 18. FINANCIAL HEALTH PROBABILITIES
    # ========================================================

    probabilities = (
        financial_health_model.predict_proba(
            encoded_input
        )[0]
    )


    probability_dictionary = {}

    for class_name, probability in zip(
        financial_health_model.classes_,
        probabilities
    ):

        probability_dictionary[
            class_name
        ] = probability


    user[
        "Financial_Health_Probabilities"
    ] = [
        probability_dictionary
    ]


    # ========================================================
    # 19. OVERALL RECOMMENDATIONS
    # ========================================================

    overall_recommendations = []


    # --------------------------------------------------------
    # Expense recommendations
    # --------------------------------------------------------

    overall_recommendations.extend(
        expense_recommendations
    )


    # --------------------------------------------------------
    # Savings recommendation
    # --------------------------------------------------------

    overall_recommendations.extend(
        savings_recommendations
    )


    # --------------------------------------------------------
    # Debt recommendation
    # --------------------------------------------------------

    overall_recommendations.append(
        debt_recommendation
    )


    # --------------------------------------------------------
    # Financial health recommendation
    # --------------------------------------------------------

    health = (
        user[
            "Financial_Health"
        ].iloc[0]
    )


    if health == "Healthy":

        overall_recommendations.append(
            "Your overall financial health is healthy. "
            "Continue maintaining your current financial "
            "habits and savings discipline."
        )

    elif health == "Moderate":

        overall_recommendations.append(
            "Your overall financial health is moderate. "
            "Review the highlighted expense, savings, "
            "and debt areas to improve your financial position."
        )

    else:

        overall_recommendations.append(
            "Your overall financial health needs improvement. "
            "Focus on controlling expenses, managing debt, "
            "and improving your savings position."
        )


    user[
        "Overall_Recommendations"
    ] = [
        overall_recommendations
    ]


    # ========================================================
    # 20. RETURN COMPLETE ANALYSIS
    # ========================================================

    return user