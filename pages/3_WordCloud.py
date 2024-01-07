import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


conn = st.connection("postgresql", type="sql")

df_skill = conn.query("SELECT skill,job_description FROM job WHERE skill IS NOT NULL ;", ttl="10m")
df_description =  conn.query("SELECT job_description FROM job WHERE job_description IS NOT NULL;", ttl="10m")

df_skill = pd.DataFrame(df_skill)
df_description = pd.DataFrame(df_description)

all_skills = ' '.join(df_skill['skill'])

job_des = ' '.join(df_description['job_description'])


col1, col2 = st.columns((2))

with col1:
    # Generate Word Cloud
    skill_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_skills)
    # Plot the Word Cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(skill_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud cho skill')

    st.pyplot(plt)
    
with col2:
    # Generate Word Cloud
    des_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(job_des)
    # Plot the Word Cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(des_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud cho job_description')
    st.pyplot(plt)



    