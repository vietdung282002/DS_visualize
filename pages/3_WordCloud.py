import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


conn = st.connection("postgresql", type="sql")

df = conn.query("SELECT skill FROM job WHERE skill IS NOT NULL;", ttl="10m")

df = pd.DataFrame(df)
all_skills = ' '.join(df['skill'])

# Generate Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_skills)

# Plot the Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for skill Column')

st.pyplot(plt)