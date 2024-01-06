import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import geopandas as gpd
from geopy.geocoders import Nominatim
# from folium.plugins import HeatMap
from streamlit_folium import folium_static
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

conn = st.connection("postgresql", type="sql")

# df = conn.query("SELECT industry,address FROM job;", ttl="10m")
industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))

# data = pd.DataFrame(df)

selected_industries = st.multiselect("Select Industries", industry )
 

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT address, COUNT(industry) AS job_count FROM job WHERE industry IN ({selected_industries}) AND address != 'Nhật Bản' AND address != 'Nước Ngoài' GROUP BY address;"
else:
    query = "SELECT address, COUNT(industry) AS job_count FROM job WHERE address != 'Nhật Bản' AND address != 'Nước Ngoài' GROUP BY address;"

df = pd.DataFrame(conn.query(query))
# def create_heatmap(address, count):
#     # Create a base map centered at the geographical center of Vietnam
#     map_center = [14.0583, 108.2772]
#     job_map = folium.Map(location=map_center, zoom_start=6)

#     # Create a list of coordinates from the provided addresses
#     coordinates = []
#     for addr in address:
#         location = [float(coord.strip()) for coord in addr.split(',')]
#         coordinates.append(location)

#     # Combine coordinates with job count
#     data = list(zip(coordinates, count))

#     # Add heatmap layer to the map
#     HeatMap(data).add_to(job_map)

#     return job_map

# st.title("Job Distribution Heat Map in Vietnam")

# job_map = create_heatmap(df['address'], df['count'])
# # Display the map using Streamlit
# folium_static(job_map)


# Sample data
data = df

# Load the GeoJSON file with Vietnam's boundaries
vietnam_geojson_path = 'vietnam.geojson'
vietnam = gpd.read_file(vietnam_geojson_path)

# Merge the GeoDataFrame with job data
df = gpd.GeoDataFrame({'address': data['address'], 'job_count': data['job_count']})
merged = vietnam.set_index('name').join(df.set_index('address'))

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Plot the base map
vietnam.boundary.plot(ax=ax, linewidth=1)

# Plot the job distribution as a choropleth map
merged.plot(column='job_count', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True, cax=cax)

# Set plot title and legend
plt.title('Job Distribution in Vietnam')
plt.show()
st.pyplot(plt)