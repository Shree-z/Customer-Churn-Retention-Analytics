import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("📊 Customer Churn & Retention Analytics")

st.write(
    "Interactive dashboard for analyzing telecom customer "
    "churn, customer behavior, and predicted churn risk."
)


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    connection = sqlite3.connect("customer_churn.db")

    query = """
    SELECT *
    FROM customers
    """

    data = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return data


df = load_data()


# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("Filters")

# Telecom partner filter
partners = sorted(
    df["telecom_partner"].dropna().unique()
)

selected_partners = st.sidebar.multiselect(
    "Telecom Partner",
    partners,
    default=partners
)

# Gender filter
genders = sorted(
    df["gender"].dropna().unique()
)

selected_genders = st.sidebar.multiselect(
    "Gender",
    genders,
    default=genders
)

# Apply filters
filtered_df = df[
    df["telecom_partner"].isin(selected_partners)
    &
    df["gender"].isin(selected_genders)
]


# ==================================================
# KPI CALCULATIONS
# ==================================================

total_customers = len(filtered_df)

churned_customers = int(
    filtered_df["churn"].sum()
)

retained_customers = (
    total_customers - churned_customers
)

if total_customers > 0:

    churn_rate = (
        churned_customers /
        total_customers
    ) * 100

else:

    churn_rate = 0


retention_rate = 100 - churn_rate


# ==================================================
# KPI DISPLAY
# ==================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Churned Customers",
        f"{churned_customers:,}"
    )

with col3:
    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col4:
    st.metric(
        "Retention Rate",
        f"{retention_rate:.2f}%"
    )


st.divider()


# ==================================================
# CHURN BY TELECOM PARTNER
# ==================================================

st.subheader("Churn Rate by Telecom Partner")

partner_data = (
    filtered_df
    .groupby("telecom_partner")["churn"]
    .mean()
    .mul(100)
    .reset_index()
)

partner_data.columns = [
    "telecom_partner",
    "churn_rate"
]

fig1, ax1 = plt.subplots(
    figsize=(8, 5)
)

sns.barplot(
    data=partner_data,
    x="telecom_partner",
    y="churn_rate",
    ax=ax1
)

ax1.set_xlabel("Telecom Partner")
ax1.set_ylabel("Churn Rate (%)")
ax1.set_title("Churn Rate by Telecom Partner")

plt.xticks(rotation=20)

st.pyplot(fig1)


# ==================================================
# CHURN BY AGE GROUP
# ==================================================

st.subheader("Churn Rate by Age Group")

age_data = (
    filtered_df
    .groupby("age_group", observed=True)["churn"]
    .mean()
    .mul(100)
    .reset_index()
)

age_data.columns = [
    "age_group",
    "churn_rate"
]

fig2, ax2 = plt.subplots(
    figsize=(10, 5)
)

sns.barplot(
    data=age_data,
    x="age_group",
    y="churn_rate",
    ax=ax2
)

ax2.set_xlabel("Age Group")
ax2.set_ylabel("Churn Rate (%)")
ax2.set_title("Churn Rate by Age Group")

st.pyplot(fig2)


# ==================================================
# CHURN BY GENDER
# ==================================================

st.subheader("Churn Rate by Gender")

gender_data = (
    filtered_df
    .groupby("gender")["churn"]
    .mean()
    .mul(100)
    .reset_index()
)

gender_data.columns = [
    "gender",
    "churn_rate"
]

fig3, ax3 = plt.subplots(
    figsize=(7, 5)
)

sns.barplot(
    data=gender_data,
    x="gender",
    y="churn_rate",
    ax=ax3
)

ax3.set_xlabel("Gender")
ax3.set_ylabel("Churn Rate (%)")
ax3.set_title("Churn Rate by Gender")

st.pyplot(fig3)


# ==================================================
# RISK SEGMENTS
# ==================================================

st.subheader("Predicted Customer Risk Segments")

risk_data = (
    filtered_df["risk_level"]
    .value_counts()
    .reindex(
        [
            "Lower Predicted Risk",
            "Medium Predicted Risk",
            "Higher Predicted Risk"
        ]
    )
    .fillna(0)
    .reset_index()
)

risk_data.columns = [
    "risk_level",
    "customers"
]

fig4, ax4 = plt.subplots(
    figsize=(9, 5)
)

sns.barplot(
    data=risk_data,
    x="risk_level",
    y="customers",
    ax=ax4
)

ax4.set_xlabel("Risk Segment")
ax4.set_ylabel("Number of Customers")
ax4.set_title("Predicted Customer Risk Segments")

plt.xticks(rotation=15)

st.pyplot(fig4)


# ==================================================
# USAGE COMPARISON
# ==================================================

st.subheader("Customer Usage by Churn Status")

usage_data = (
    filtered_df
    .groupby("churn")
    [
        [
            "calls_made",
            "sms_sent",
            "data_used"
        ]
    ]
    .mean()
    .reset_index()
)

usage_data["churn_status"] = (
    usage_data["churn"]
    .map({
        0: "Retained",
        1: "Churned"
    })
)

st.dataframe(
    usage_data[
        [
            "churn_status",
            "calls_made",
            "sms_sent",
            "data_used"
        ]
    ].round(2),
    use_container_width=True
)


# ==================================================
# HIGHER PREDICTED-RISK CUSTOMERS
# ==================================================

st.subheader("Higher Predicted-Risk Customers")

high_risk = filtered_df[
    filtered_df["risk_level"]
    == "Higher Predicted Risk"
].copy()

high_risk = high_risk.sort_values(
    "churn_probability",
    ascending=False
)

display_columns = [
    "customer_id",
    "telecom_partner",
    "gender",
    "age",
    "state",
    "estimated_salary",
    "calls_made",
    "sms_sent",
    "data_used",
    "churn_probability",
    "risk_level"
]

st.dataframe(
    high_risk[
        display_columns
    ].head(100),
    use_container_width=True
)


# ==================================================
# BUSINESS INSIGHTS
# ==================================================

st.subheader("Business Interpretation")

st.markdown(
    """
### Recommended analytical actions

- Monitor customer segments with higher observed churn rates.
- Prioritize customers with higher predicted churn probabilities
  for retention outreach.
- Investigate usage patterns associated with observed churn.
- Compare customer behavior across telecom partners and regions.
- Use the dashboard filters to investigate specific customer segments.

**Note:** Predicted risk represents model output and does not
guarantee that an individual customer will churn.
"""
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Customer Churn & Retention Analytics | "
    "Python + SQL + Machine Learning"
)