import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


conn = st.connection("postgresql", type="sql")

df = conn.query("SELECT * FROM job;", ttl="10m")

industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))
location = pd.DataFrame(conn.query("SELECT DISTINCT job_address FROM job;"))

# if selected_industries:
df = pd.DataFrame(df)

# Streamlit app
st.title("Education Level")
selected_industries = st.multiselect("Select Industries", industry )

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT job_level,COUNT(*) AS count FROM job WHERE industry IN ({selected_industries}) and job_level!= 'not-found' GROUP BY job_level"
else:
    query = f"SELECT job_level,COUNT(*) AS count FROM job where job_level!= 'not-found' GROUP BY job_level"
    
df = pd.DataFrame(conn.query(query))
st.subheader(f"Job level count ")
fig = px.bar(
        df,
        x='job_level',
        y='count',
        text='count', 
        labels={'job_level': 'Job_level', 'count': 'Number of Jobs'},
        color='job_level',
        height=500,
    )
st.plotly_chart(fig,use_container_width=True, height =300)