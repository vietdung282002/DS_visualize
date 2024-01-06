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
    query = f"SELECT industry,gender FROM job WHERE industry IN ({selected_industries}) "
else:
    query = f"SELECT industry,gender FROM job "
col1, col2 = st.columns((2))

df = pd.DataFrame(conn.query(query))

table = pd.crosstab(df['industry'], df['gender'])

# Plotting the stacked bar chart
fig, ax = plt.subplots()
table.plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'lightcoral'])
# Adding labels and title
ax.set_xlabel('Industry')
ax.set_ylabel('Count')
ax.set_title('Gender Distribution in Each Industry')
# Adding legend
ax.legend(title='Gender')
# Display the plot
st.pyplot(fig)