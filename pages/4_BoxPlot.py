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
    query = f"SELECT salary_min,salary_max,yoe_min,yoe_max FROM job WHERE industry IN ({selected_industries}) "
else:
    query = f"SELECT salary_min,salary_max,yoe_min,yoe_max FROM job "

df = pd.DataFrame(conn.query(query))
    
df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")/1000000
df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")/1000000

# Create a boxplot
filtered_df = df[(df["salary_min"] < 100) & (df["salary_max"] < 100)]

fig, ax = plt.subplots()
ax.boxplot([filtered_df["salary_min"].dropna(), filtered_df["salary_max"].dropna()], labels=["Min Salary", "Max Salary"])
ax.set_title("Salary Distribution")
ax.set_ylabel("Salary (triệu VND)")

# Display the boxplot using Streamlit
st.pyplot(fig)