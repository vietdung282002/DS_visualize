import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


conn = st.connection("postgresql", type="sql")

df = conn.query("SELECT * FROM job;", ttl="10m")

industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))
location = pd.DataFrame(conn.query("SELECT DISTINCT address FROM job;"))

# if selected_industries:
df = pd.DataFrame(df)

# Streamlit app
st.title("Education Level Histogram")
selected_industries = st.multiselect("Select Industries", industry )

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT education_level,industry,gender FROM job WHERE industry IN ({selected_industries}) "
else:
    query = f"SELECT education_level,industry,gender FROM job "
col1, col2 = st.columns((2))

df = pd.DataFrame(conn.query(query))

with col1:
    st.subheader('Distribution of Education Levels')
    fig_edu = plt.figure(figsize=(11, 7))
    plt.hist(df['education_level'], bins=29, color='skyblue')
    plt.title('Education Levels')
    plt.xlabel('Education Level')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90, ha='right')
    st.pyplot(fig_edu)
      
with col2:
    st.subheader('Distribution of Gender')
    fig_gen = plt.figure(figsize=(11, 7))
    plt.hist(df['gender'], bins=3, color='lightgreen')
    plt.title('Gender')
    plt.xlabel('Gender')
    plt.ylabel('Frequency')
    st.pyplot(fig_gen)
