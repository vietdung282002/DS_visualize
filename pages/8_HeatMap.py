import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from unidecode import unidecode
from fuzzywuzzy import process

province = [
    "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh",
    "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cao Bằng",
    "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",
    "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa",
    "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An",
    "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Quảng Bình", "Quảng Nam",
    "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình",
    "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh", "Tuyên Quang",
    "Vĩnh Long", "Vĩnh Phúc", "Yên Bái", "Phú Yên", "Cần Thơ", "Đà Nẵng", "Hải Phòng",
    "Hà Nội", "Hồ Chí Minh"
]

def chuan_hoa_ten(ten):
    ten_moi = ""
    for i in range(len(ten) - 1):
        if ten[i].islower() and ten[i+1].isupper():
            ten_moi += ten[i] + " "
        else:
            ten_moi += ten[i]
    ten_moi += ten[-1]
    return ten_moi

def tim_kiem_tinh_co_dau(query):
    matches = process.extractOne(query, province)
    return province[province.index(matches[0])]

conn = st.connection("postgresql", type="sql")

# df = conn.query("SELECT industry,address FROM job;", ttl="10m")
industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))

# data = pd.DataFrame(df)

selected_industries = st.multiselect("Select Industries", industry )
 

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT job_address, COUNT(industry) AS job_count FROM job WHERE industry IN ({selected_industries}) AND job_address != 'Nhật Bản' AND job_address != 'Nước Ngoài' GROUP BY job_address;"
else:
    query = "SELECT job_address, COUNT(industry) AS job_count FROM job WHERE job_address != 'Nhật Bản' AND job_address != 'Nước Ngoài' GROUP BY job_address;"

df = pd.DataFrame(conn.query(query))

df['job_address'] =  df['job_address'].apply(chuan_hoa_ten).apply(tim_kiem_tinh_co_dau)

data = df

# Load the GeoJSON file with Vietnam's boundaries
vietnam_geojson_path = 'vietnam.geojson'
vietnam = gpd.read_file(vietnam_geojson_path)

# Merge the GeoDataFrame with job data
df = gpd.GeoDataFrame({'job_address': data['job_address'], 'job_count': data['job_count']})
merged = vietnam.set_index('name').join(df.set_index('job_address'))

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Plot the base map
vietnam.boundary.plot(ax=ax, linewidth=0.5)

# Plot the job distribution as a choropleth map
merged.plot(column='job_count', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, cax=cax)

# Set plot title and legend
plt.title('Job Distribution in Vietnam')
plt.show()
st.pyplot(plt)