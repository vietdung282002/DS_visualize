import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu từ tệp CSV
file_path = r"D:\Codepython\Data Science\New folder\DS_visualize\job.csv"
df = pd.read_csv(file_path)

# Tiêu đề cho trang
st.title("Phân Loại Ngành theo Địa Chỉ")

# Sidebar cho việc chọn địa chỉ
selected_address = st.sidebar.selectbox("Chọn Địa Chỉ", df['address'].unique())

# Lọc dữ liệu theo địa chỉ được chọn
filtered_df = df[df['address'] == selected_address]

# Phân loại ngành theo địa chỉ được chọn
industry_counts = filtered_df['industry'].value_counts()

# Hiển thị dữ liệu
st.write(f"Phân loại ngành cho địa chỉ {selected_address}:")
st.write(industry_counts)

# Vẽ biểu đồ cột
fig = px.bar(
    x=industry_counts.index,
    y=industry_counts.values,
    labels={'x': 'Ngành Nghề', 'y': 'Số Lượng Công Việc'},
    title=f"Phân Loại Ngành Cho Địa Chỉ {selected_address}",
)
st.plotly_chart(fig, use_container_width=True)