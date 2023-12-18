import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt


#streamlit run .\main.py --server.port 8888

st.set_page_config(page_title="Job", page_icon=":barchart:",layout="wide")
st.title(" :bar_chart: Job dashboard")
st.markdown('<style>div.block-container{padding-top: 1rem}</style>',unsafe_allow_html=True)

