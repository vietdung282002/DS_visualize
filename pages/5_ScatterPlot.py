import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

conn = st.connection("postgresql", type="sql")

df = conn.query("SELECT * FROM job;", ttl="10m")

industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))

# if selected_industries:
df = pd.DataFrame(df)

# Streamlit app
selected_industries = st.multiselect("Select Industries", industry )

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT salary_min,salary_max,job_yoe_min,job_yoe_max FROM job WHERE industry IN ({selected_industries}) "
else:
    query = f"SELECT salary_min,salary_max,job_yoe_min,job_yoe_max FROM job "

df = pd.DataFrame(conn.query(query))
    
df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")/1000000
df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")/1000000
df["job_yoe_min"] = pd.to_numeric(df["job_yoe_min"], errors="coerce")
df["job_yoe_max"] = pd.to_numeric(df["job_yoe_max"], errors="coerce")

df = df[(df["salary_min"] < 100) & (df["salary_max"] < 100)]

col1, col2 = st.columns((2))

with col1:
    fig, ax = plt.subplots()
    sc = ax.scatter(df["salary_min"], df["salary_max"], c=df["job_yoe_min"], cmap="viridis", s=100, alpha=0.75, marker='o')
    ax.set_xlabel("Min Salary (triệu VND)")
    ax.set_ylabel("Max Salary (triệu VND)")
    ax.set_title("Phụ thuộc số năm kinh nghiệm của mức lương")

    # Add colorbar
    cbar = plt.colorbar(sc, ax=ax, label="Years of Experience (Min)")

    # Display the scatter plot using Streamlit
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    sc = ax.scatter(df["salary_min"], df["salary_max"], c=df["job_yoe_max"], cmap="viridis", s=100, alpha=0.75, marker='o')
    ax.set_xlabel("Min Salary (triệu VND)")
    ax.set_ylabel("Max Salary (triệu VND)")
    ax.set_title("Phụ thuộc số năm kinh nghiệm của mức lương")

    # Add colorbar
    cbar = plt.colorbar(sc, ax=ax, label="Years of Experience (Max)")

    # Display the scatter plot using Streamlit
    st.pyplot(fig)