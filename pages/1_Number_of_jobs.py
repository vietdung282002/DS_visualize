import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

conn = st.connection("postgresql", type="sql")
st.title("Nhu cầu tuyển dụng của các ngành nghề tại các tỉnh thành")


df = conn.query("SELECT * FROM job;", ttl="10m")

industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))
location = pd.DataFrame(conn.query("SELECT DISTINCT address FROM job;"))

data = pd.DataFrame(df)
col1, col2 = st.columns((2))

with col1:
    selected_industries = st.multiselect("Select Industries", industry )
with col2:
    selected_city = st.multiselect("Select Address", location)


st.dataframe(location)
if selected_industries and selected_city:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    selected_city = ', '.join(map(lambda x: f"'{x}'", selected_city))
    query = f"SELECT industry, COUNT(*) AS count FROM job WHERE industry IN ({selected_industries}) AND address IN ({selected_city}) GROUP BY industry;"
elif selected_industries and not selected_city: 
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT industry, COUNT(*) AS count FROM job WHERE industry IN ({selected_industries}) GROUP BY industry;"
elif selected_city and not selected_industries:
    selected_city = ', '.join(map(lambda x: f"'{x}'", selected_city))
    query = f"SELECT industry, COUNT(*) AS count FROM job WHERE address IN ({selected_city}) GROUP BY industry;"
else:
    query = "SELECT industry, COUNT(*) AS count FROM job GROUP BY industry;"


industry_counts = pd.DataFrame(conn.query(query))
industry_counts.columns = ['industry', 'count']


with col1:
    st.subheader(f"Number of Jobs in Each Industry ")
    fig = px.bar(
            industry_counts,
            x='industry',
            y='count',
            text='count', 
            labels={'industry': 'Industry', 'count': 'Number of Jobs'},
            color='industry',
            height=500,
        )
    st.plotly_chart(fig,use_container_width=True, height =300)
    
with col2:
    st.subheader("Percentage of Jobs in Each Industry")
    fig = px.pie(
        industry_counts,
        values='count',
        names='industry',
        labels={'industry': 'Industry'},
        height=500,
    )
    st.plotly_chart(fig,use_container_width=True, height =300)
    