import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu từ tệp CSV
file_path = r"D:\Codepython\Data Science\New folder\DS_visualize\job.csv"
df = pd.read_csv(file_path)

# Tiêu đề cho trang
st.title("Phân Loại Tỉ Lệ Nam/Nữ theo Ngành Nghề")

# Sidebar cho việc chọn ngành nghề
selected_industry = st.sidebar.selectbox("Chọn Ngành Nghề", df['industry'].unique())

# Tính tỉ lệ nam/nữ theo ngành nghề
gender_by_industry = df[df['industry'] == selected_industry].groupby('gender').size()

# Hiển thị dữ liệu
st.write(f"Tỉ Lệ Nam/Nữ cho Ngành Nghề {selected_industry}:")
st.write(gender_by_industry)

# Vẽ biểu đồ tròn
st.subheader("Biểu Đồ Tròn")
fig = px.pie(
    values=gender_by_industry.values,
    names=gender_by_industry.index,
    title=f"Tỉ Lệ Nam/Nữ cho Ngành Nghề {selected_industry}",
)
st.plotly_chart(fig, use_container_width=True)
