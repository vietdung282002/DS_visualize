import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

conn = st.connection("postgresql", type="sql")
st.title("Nhu cầu tuyển dụng của các ngành nghề tại các tỉnh thành")

industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))
location = pd.DataFrame(conn.query("SELECT DISTINCT job_address FROM job where job_address != 'not-found';"))
col1, col2 = st.columns((2))

with col1:
    selected_industries = st.multiselect("Select Industries", industry )
with col2:
    selected_city = st.multiselect("Select Address", location)


if selected_industries and selected_city:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    selected_city = ', '.join(map(lambda x: f"'{x}'", selected_city))
    query = f"SELECT job_address, COUNT(*) AS count FROM job WHERE industry IN ({selected_industries}) AND job_address IN ({selected_city}) GROUP BY job_address;"
elif selected_industries and not selected_city: 
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT job_address, COUNT(*) AS count FROM job WHERE industry IN ({selected_industries}) and job_address != 'not-found' GROUP BY job_address;"
elif selected_city and not selected_industries:
    selected_city = ', '.join(map(lambda x: f"'{x}'", selected_city))
    query = f"SELECT job_address, COUNT(*) AS count FROM job WHERE job_address IN ({selected_city}) GROUP BY job_address;"
else:
    query = "SELECT job_address, COUNT(*) AS count FROM job where job_address != 'not-found' GROUP BY job_address;"
    
industry_counts = pd.DataFrame(conn.query(query))

industry_counts.columns = ['job_address', 'count']


with col1:
    st.subheader(f"Number of Jobs in Each Industry")
    fig = px.bar(
            industry_counts,
            x='job_address',
            y='count',
            text='count', 
            labels={'job_address': 'Job_address', 'count': 'Number of Jobs'},
            color='job_address',
            height=500,
            title=f"Number of Jobs recuitment"
        )
    st.plotly_chart(fig,use_container_width=True, height =300)
    
with col2:
    st.subheader("Percentage of Jobs in Each Industry")
    fig = px.pie(
        industry_counts,
        values='count',
        names='job_address',
        labels={'job_address': 'Job_address'},
        height=500,
    )
    st.plotly_chart(fig,use_container_width=True, height =300)