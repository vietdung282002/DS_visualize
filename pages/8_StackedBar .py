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
col1, col2 = st.columns((2))

# Streamlit app

with col2:
    selected_industries2 = st.selectbox("Chọn Ngành Nghề", df['industry'].unique())
    

query = f"SELECT industry,gender FROM job "

if selected_industries2:
    query2 = f"SELECT gender, COUNT(*) AS count FROM job WHERE industry = '{selected_industries2}' GROUP BY gender;"
    

    
df = pd.DataFrame(conn.query(query))
df2 = pd.DataFrame(conn.query(query2))


df['gender'] = df['gender'].fillna('Unknown')
df2['gender'] = df2['gender'].fillna('Unknown')


# Tạo bảng chéo
table = pd.crosstab(df['industry'], df['gender'])

with col1:
# Plotting the stacked bar chart
    fig, ax = plt.subplots()
    table.plot(kind='bar', stacked=True, ax=ax, color=['blue', 'orange','pink', 'green'])
    # Adding labels and title
    ax.set_xlabel('Industry')
    ax.set_ylabel('Count')
    ax.set_title('Phân phối tỷ lệ tuyển dụng giới tính')
    # Adding legend
    ax.legend(title='Gender')
    # Display the plot
    st.pyplot(fig)
    
with col2:
    st.subheader(f"Tỷ lệ tuyển dụng giới tính ngành {selected_industries2}")
    fig = px.pie(
        df2,
        values='count',
        names='gender',
        labels={'gender': 'Industry'},
        height=500,
        
    )
    st.plotly_chart(fig,use_container_width=True, height =300)
