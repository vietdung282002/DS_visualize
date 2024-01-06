import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu từ tệp CSV
file_path = r"D:\Codepython\Data Science\New folder\DS_visualize\job.csv"
df = pd.read_csv(file_path)

# Tiêu đề cho trang
st.title("Phân Loại Công Việc theo Ngành và Trình Độ Yêu Cầu")

# Chọn ngành nghề
selected_industries = st.multiselect("Chọn Ngành Nghề", df['industry'].unique())

# Lọc dữ liệu theo ngành nghề đã chọn
filtered_df = df[df['industry'].isin(selected_industries)]

# Phân loại công việc theo ngành và trình độ yêu cầu
industry_education_counts = filtered_df.groupby(['industry', 'education_level']).size().unstack(fill_value=0)

# Lọc các trình độ lớn hơn 0 cho mỗi ngành
industry_education_counts = industry_education_counts[industry_education_counts > 0].stack().unstack(fill_value=0)

# Hiển thị dữ liệu
st.write("Số lượng công việc theo ngành và trình độ yêu cầu:")

# Loại bỏ các cột không có dữ liệu
industry_education_counts = industry_education_counts.loc[:, (industry_education_counts != 0).any(axis=0)]

st.write(industry_education_counts)

# Vẽ biểu đồ heatmap
st.subheader("Biểu Đồ Heatmap")
fig = px.imshow(
    industry_education_counts,
    labels=dict(x="Trình Độ Yêu Cầu", y="Ngành Nghề", color="Số Lượng Công Việc"),
    x=industry_education_counts.columns,
    y=industry_education_counts.index,
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig, use_container_width=True)
