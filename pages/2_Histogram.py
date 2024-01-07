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
    query = f"SELECT education_level,industry FROM job WHERE industry IN ({selected_industries}) AND education_level IS NOT NULL "
else:
    query = f"SELECT education_level,industry FROM job WHERE education_level IS NOT NULL"


df = pd.DataFrame(conn.query(query))
col1, col2 = st.columns((2))

with col1:
    st.subheader('Histogram Distribution of Education Levels')
    fig_edu = plt.figure(figsize=(11, 7))
    plt.hist(df['education_level'], bins=35, edgecolor='black')
    plt.title(f'Phân phối Education Levels')
    plt.xlabel('Education Levels')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    st.pyplot(fig_edu)
    
industry_education_counts = df.groupby(['industry', 'education_level']).size().unstack(fill_value=0)

# Lọc các trình độ lớn hơn 0 cho mỗi ngành
industry_education_counts = industry_education_counts[industry_education_counts > 0].stack().unstack(fill_value=0)

# Hiển thị dữ liệu
# Loại bỏ các cột không có dữ liệu
industry_education_counts = industry_education_counts.loc[:, (industry_education_counts != 0).any(axis=0)]

# st.write(industry_education_counts)

# Vẽ biểu đồ heatmap
with col2:
    st.subheader("Heatmap")
    fig = px.imshow(
        industry_education_counts,
        labels=dict(x="Trình Độ Yêu Cầu", y="Ngành Nghề", color="Số Lượng Công Việc"),
        x=industry_education_counts.columns,
        y=industry_education_counts.index,
        color_continuous_scale="Viridis",
        height=700,
        title=(f'Phân phối Education Levels')
    )
    st.plotly_chart(fig,use_container_width=True, height =300)
