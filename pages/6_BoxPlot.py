import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = st.connection("postgresql", type="sql")

df = conn.query("SELECT * FROM job;", ttl="10m")

industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))

# if selected_industries:
df = pd.DataFrame(df)

# Streamlit app
selected_industries = st.multiselect("Select Industries", industry )

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT salary_min,salary_max,job_yoe_min, job_yoe_max FROM job WHERE industry IN ({selected_industries}) "
    salary_title = f"Phân phối mức lương ngành {selected_industries}"
    yoe_title = f"Phân phối số năm kinh nghiệm ngành {selected_industries} "
else:
    query = f"SELECT salary_min,salary_max,job_yoe_min, job_yoe_max FROM job "
    salary_title = f"Phân phối mức lương"
    yoe_title = f"Phân phối số năm kinh nghiệm"

df = pd.DataFrame(conn.query(query))
    
df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")/1000000
df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")/1000000
df["job_yoe_min"] = pd.to_numeric(df["job_yoe_min"], errors="coerce")
df["job_yoe_max"] = pd.to_numeric(df["job_yoe_max"], errors="coerce")
# Create a boxplot
filtered_df = df[(df["salary_min"] < 100) & (df["salary_max"] < 100)]

col1, col2 = st.columns((2))
with col1:

    fig, ax = plt.subplots()
    ax.boxplot([filtered_df["salary_min"].dropna(), filtered_df["salary_max"].dropna()], labels=["Min Salary", "Max Salary"])
    ax.set_title(salary_title)
    ax.set_ylabel("Salary (triệu VND)")

    # Display the boxplot using Streamlit
    st.pyplot(fig)
    
with col2:

    fig, ax = plt.subplots()
    ax.boxplot([df["job_yoe_min"].dropna(), df["job_yoe_max"].dropna()], labels=["Min", "Max"])
    ax.set_title(yoe_title)
    ax.set_ylabel("Year of experience (Year)")

    # Display the boxplot using Streamlit
    st.pyplot(fig)
    
with col1:
    fig, ax = plt.subplots()
    ax = sns.violinplot(data=filtered_df[['salary_min', 'salary_max']])
    ax.set(ylabel='Salary (triệu VND)')
    # Đặt tên cho trục x và trục y
    ax.set_title(salary_title)
    violin_names = ['Salary Min', 'Salary Max']
    for i, violin in enumerate(ax.collections):
        if i % 2 == 0:
            violin.set_label(violin_names[i // 2])

    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots()
    ax = sns.violinplot(data=df[['job_yoe_min', 'job_yoe_max']])
    ax.set(ylabel='Year of experience (Year)')
    # Đặt tên cho trục x và trục y
    ax.set_title(yoe_title)
    violin_names = ['Min', 'Max']
    for i, violin in enumerate(ax.collections):
        if i % 2 == 0:
            violin.set_label(violin_names[i // 2])

    st.pyplot(fig)