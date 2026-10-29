import streamlit as st
import pandas as pd
from adviser.financial_advisor import analyze_user_finances


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Personal Finance Advisor",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("💰 AI Personal Finance Advisor")

st.write(
    "Enter your personal and monthly financial information "
    "to receive an AI-based financial health analysis."
)


# ============================================================
# PERSONAL INFORMATION
# ============================================================

st.header("👤 Personal Information")

col1, col2, col3, col4 = st.columns(4)

with col1:

    income = st.number_input(
        "Monthly Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

with col2:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1
    )

with col3:

    dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        max_value=20,
        value=1,
        step=1
    )

with col4:

    city_tier = st.selectbox(
        "City Tier",
        [
            "Tier_1",
            "Tier_2",
            "Tier_3"
        ],
        index=1
    )


# ============================================================
# MONTHLY EXPENSES
# ============================================================

st.header("💳 Monthly Expenses")

col1, col2, col3 = st.columns(3)

with col1:

    rent = st.number_input(
        "Rent",
        min_value=0.0,
        value=10000.0,
        step=500.0
    )

    loan_repayment = st.number_input(
        "Loan Repayment",
        min_value=0.0,
        value=4000.0,
        step=500.0
    )

    insurance = st.number_input(
        "Insurance",
        min_value=0.0,
        value=1500.0,
        step=100.0
    )

    groceries = st.number_input(
        "Groceries",
        min_value=0.0,
        value=6000.0,
        step=500.0
    )


with col2:

    transport = st.number_input(
        "Transport",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )

    eating_out = st.number_input(
        "Eating Out",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )

    entertainment = st.number_input(
        "Entertainment",
        min_value=0.0,
        value=2000.0,
        step=500.0
    )

    utilities = st.number_input(
        "Utilities",
        min_value=0.0,
        value=2500.0,
        step=500.0
    )


with col3:

    healthcare = st.number_input(
        "Healthcare",
        min_value=0.0,
        value=2000.0,
        step=500.0
    )

    education = st.number_input(
        "Education",
        min_value=0.0,
        value=1500.0,
        step=500.0
    )

    miscellaneous = st.number_input(
        "Miscellaneous",
        min_value=0.0,
        value=1000.0,
        step=500.0
    )


# ============================================================
# SAVINGS
# ============================================================

st.header("💰 Savings Goal")

desired_savings = st.number_input(
    "Desired Monthly Savings",
    min_value=0.0,
    value=7500.0,
    step=500.0
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.divider()

analyze_button = st.button(
    "🔍 Analyze My Finances",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # Basic validation
    # --------------------------------------------------------

    total_expenses = (
        rent
        + loan_repayment
        + insurance
        + groceries
        + transport
        + eating_out
        + entertainment
        + utilities
        + healthcare
        + education
        + miscellaneous
    )

    if income <= 0:

        st.error(
            "Income must be greater than zero."
        )

    elif total_expenses > income * 2:

        st.warning(
            "Your entered expenses are unusually high "
            "compared with your income. Please check "
            "the values before continuing."
        )

    else:

        # ----------------------------------------------------
        # Run financial analysis
        # ----------------------------------------------------

        result = analyze_user_finances(

            income=income,
            age=age,
            dependents=dependents,
            city_tier=city_tier,

            rent=rent,
            loan_repayment=loan_repayment,
            insurance=insurance,
            groceries=groceries,
            transport=transport,
            eating_out=eating_out,
            entertainment=entertainment,
            utilities=utilities,
            healthcare=healthcare,
            education=education,
            miscellaneous=miscellaneous,

            desired_savings=desired_savings
        )


        # ====================================================
        # RESULTS
        # ====================================================

        st.divider()

        st.header("📊 Financial Analysis")


        # ----------------------------------------------------
        # Key Results
        # ----------------------------------------------------

        financial_health = result[
            "Financial_Health"
        ].iloc[0]

        total_expenses_result = result[
            "Total_Expenses"
        ].iloc[0]

        remaining_income = result[
            "Remaining_Income"
        ].iloc[0]

        savings_status = result[
            "Savings_Status"
        ].iloc[0]

        debt_status = result[
            "Debt_Status"
        ].iloc[0]


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Financial Health",
                financial_health
            )


        with col2:

            st.metric(
                "Total Expenses",
                f"₹{total_expenses_result:,.2f}"
            )


        with col3:

            st.metric(
                "Remaining Income",
                f"₹{remaining_income:,.2f}"
            )


        with col4:

            st.metric(
                "Savings Status",
                savings_status
            )


        # ====================================================
        # DEBT STATUS
        # ====================================================

        st.subheader("💳 Debt Analysis")

        st.info(
            f"**Debt Status:** {debt_status}"
        )

        debt_recommendation = result[
            "Debt_Recommendation"
        ].iloc[0]

        st.write(
            debt_recommendation
        )


        # ====================================================
        # SAVINGS ANALYSIS
        # ====================================================

        st.subheader("💰 Savings Analysis")

        detailed_savings_status = result[
            "Detailed_Savings_Status"
        ].iloc[0]

        savings_feasibility = result[
            "Savings_Feasibility"
        ].iloc[0]

        savings_buffer = result[
            "Savings_Buffer_Percentage"
        ].iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Savings Feasibility",
                f"₹{savings_feasibility:,.2f}"
            )

        with col2:

            st.metric(
                "Savings Buffer",
                f"{savings_buffer:.2f}%"
            )

        with col3:

            st.metric(
                "Detailed Status",
                detailed_savings_status
            )


        savings_recommendation = result[
            "Savings_Recommendation"
        ].iloc[0]

        for recommendation in savings_recommendation:

            st.write(
                "•",
                recommendation
            )


        # ====================================================
        # EXPENSE STATUS TABLE
        # ====================================================

        st.subheader("📋 Expense Status")

        status_data = []

        expense_categories = [
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

        for category in expense_categories:

            ratio_column = (
                category + "_Ratio"
            )

            status_column = (
                category + "_Status"
            )

            status_data.append({

                "Category":
                    category.replace("_", " "),

                "Amount":
                    result[
                        category
                    ].iloc[0],

                "Income %":
                    result[
                        ratio_column
                    ].iloc[0] * 100,

                "Status":
                    result[
                        status_column
                    ].iloc[0]
            })


        status_df = st.dataframe(
            status_data,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # OVERALL RECOMMENDATIONS
        # ====================================================

        st.subheader("📝 Overall Recommendations")

        overall_recommendations = result[
            "Overall_Recommendations"
        ].iloc[0]

        for recommendation in overall_recommendations:

            st.write(
                "•",
                recommendation
            )


        # ====================================================
        # MODEL PROBABILITIES
        # ====================================================

        st.subheader(
            "🤖 Financial Health Prediction Probabilities"
        )

        probabilities = result[
            "Financial_Health_Probabilities"
        ].iloc[0]

        probability_data = {

            class_name:
                f"{probability:.2%}"

            for class_name, probability
            in probabilities.items()
        }

        st.dataframe(
            pd.DataFrame(
                [probability_data]
            ),
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # SUCCESS MESSAGE
        # ====================================================

        st.success(
            "Financial analysis completed successfully."
        )