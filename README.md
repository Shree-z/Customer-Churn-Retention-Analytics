# Customer Churn & Retention Analytics

## 1. Project Overview

Customer churn is a major challenge for telecom companies because losing existing customers can affect revenue and long-term customer relationships.

This project analyzes telecom customer data to identify the key factors associated with customer churn, identify customers in different predicted-risk segments, and provide data-driven recommendations that can support customer retention strategies.

The project follows the complete data analytics workflow:

**Data → Information → Insights → Decision → Action**

The project combines:

- Python for data analysis and machine learning
- SQL for data querying and KPI analysis
- Machine Learning for churn prediction
- Streamlit for interactive dashboard visualization

---

## 2. Project Objective

The main objective of this project is:

> **Analyze customer behavior to identify the key factors responsible for customer churn, identify high-risk customer segments, and provide data-driven recommendations to improve customer retention.**

The project aims to answer questions such as:

- What percentage of customers have churned?
- Which telecom partners have higher churn rates?
- How does churn vary across customer demographics?
- How do customer usage patterns differ between churned and retained customers?
- Which customer groups have higher predicted churn risk?
- Which factors can be considered when designing customer retention strategies?

---

## 3. Dataset

The project uses a Telecom Churn Dataset containing customer-level telecom information.

### Dataset Source

Kaggle:

https://www.kaggle.com/datasets/suraj520/telecom-churn-dataset

### Dataset Features

The dataset contains the following columns:

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `telecom_partner` | Telecom service provider/partner |
| `gender` | Customer gender |
| `age` | Customer age |
| `state` | Customer state |
| `city` | Customer city |
| `pincode` | Customer pincode |
| `date_of_registration` | Customer registration date |
| `num_dependents` | Number of customer dependents |
| `estimated_salary` | Estimated customer salary |
| `calls_made` | Number of calls made |
| `sms_sent` | Number of SMS messages sent |
| `data_used` | Amount of data used |
| `churn` | Customer churn indicator |

The target variable used for machine learning is:

```text
churn