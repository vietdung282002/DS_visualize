import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

conn = st.connection("postgresql", type="sql")



industry = pd.DataFrame(conn.query("SELECT DISTINCT industry FROM job;"))
selected_industries = st.multiselect("Select Industries", industry )

if selected_industries:
    selected_industries = ', '.join(map(lambda x: f"'{x}'", selected_industries))
    query = f"SELECT industry,yoe_min,yoe_max FROM job WHERE industry IN ({selected_industries});"
else:
    query = f"SELECT industry,yoe_min,yoe_max FROM job;"
    
df = conn.query(query, ttl="10m")
# 
df = pd.DataFrame(df)


plt.figure(figsize=(10, 6))
df.boxplot(column=['yoe_min', 'yoe_max'], vert=False, patch_artist=True,)
plt.title('Distribution of Years of Experience (yoe_min and yoe_max)')
plt.xlabel('Years of Experience')

st.pyplot(plt)
