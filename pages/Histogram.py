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

# Display the data
selected_industry = st.sidebar.selectbox("Select Industries", industry)
selected_city = st.sidebar.multiselect("Select Address", location)

# Filter data based on selected industry
df = df[df['industry'] == selected_industry]
# Create a histogram of education levels
st.subheader("Histogram of Education Levels")
fig, ax = plt.subplots(figsize=(8,6))
df['education_level'].value_counts().plot(kind='bar', ax=ax)
ax.set_xlabel('Education Level')
ax.set_ylabel('Count')
st.pyplot(fig)