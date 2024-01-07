import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu từ tệp CSV
file_path = r"job.csv"
df = pd.read_csv(file_path)

# Tiêu đề cho trang
st.title("Phân Loại Tỉ Lệ Hình Thức Làm Việc theo Ngành Nghề")

# Sidebar cho việc chọn ngành nghề
selected_industry = st.sidebar.selectbox("Chọn Ngành Nghề", df['industry'].unique())

# Tính tỉ lệ hình thức làm việc theo ngành nghề
employment_type_by_industry = df[df['industry'] == selected_industry].groupby('employment_type').size()

# Hiển thị dữ liệu
st.write(f"Tỉ Lệ Hình Thức Làm Việc cho Ngành Nghề {selected_industry}:")
st.write(employment_type_by_industry)

# Vẽ biểu đồ tròn
st.subheader("Biểu Đồ Tròn")
fig = px.pie(
    values=employment_type_by_industry.values,
    names=employment_type_by_industry.index,
    title=f"Tỉ Lệ Hình Thức Làm Việc cho Ngành Nghề {selected_industry}",
)
st.plotly_chart(fig, use_container_width=True)
