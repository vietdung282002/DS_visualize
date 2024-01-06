# File: analyze_job_by_industry.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu từ tệp CSV
file_path = r"D:\Codepython\Data Science\New folder\DS_visualize\job.csv"
df = pd.read_csv(file_path)

# Tiêu đề cho trang
st.title("Phân Tích Số Lượng Công Việc theo Ngành Nghề")

# Phân tích số lượng công việc cho mỗi ngành nghề
industry_counts = df['industry'].value_counts()

# Hiển thị dữ liệu
st.write("Số lượng công việc theo ngành nghề:")
st.write(industry_counts)

# Vẽ biểu đồ cột hoặc biểu đồ tròn
chart_type = st.radio("Chọn loại biểu đồ:", ["Biểu đồ cột", "Biểu đồ tròn"])

if chart_type == "Biểu đồ cột":
    st.subheader("Biểu Đồ Cột")
    fig = px.bar(
        x=industry_counts.index,
        y=industry_counts.values,
        labels={'x': 'Ngành Nghề', 'y': 'Số Lượng Công Việc'},
        title="Phân Phối Số Lượng Công Việc theo Ngành Nghề",
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Biểu đồ tròn":
    st.subheader("Biểu Đồ Tròn")
    fig = px.pie(
        values=industry_counts.values,
        names=industry_counts.index,
        title="Tỉ Lệ Công Việc theo Ngành Nghề",
    )
    st.plotly_chart(fig, use_container_width=True)