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


df = pd.DataFrame(conn.query(query))


st.subheader('Distribution of Education Levels')
fig_edu = plt.figure(figsize=(11, 7))
plt.hist(df['education_level'], bins=20)
plt.title('Education Levels')
plt.xlabel('Education Level')
plt.ylabel('Frequency')
plt.xticks(rotation=90, ha='right')
st.pyplot(fig_edu)