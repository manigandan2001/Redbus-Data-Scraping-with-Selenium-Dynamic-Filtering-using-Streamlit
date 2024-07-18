import json
import requests
import streamlit as st 
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
)

st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        Welcome to the Homepage of 
        <span style='color: red;'>Redbus Data Scraping</span> 
        <span style='color: white;'>with</span> 
        <span style='color: red;'>Selenium</span> 
        <span style='color: white;'>and</span> 
        <span style='color: red;'>Dynamic Filtering</span> 
        <span style='color: white;'>using Streamlit</span>
    </h1>
    """, 
    unsafe_allow_html=True
)
st.sidebar.success("Select a page from above")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/28ab51fe-7e2f-4996-a8cf-17c089c8e603/mFId1gNFg3.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low"
)

st.write("""The "Redbus Data Scraping and Filtering with Streamlit Application" aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.
""")
st.markdown("<span style='color: red;'>Domain:</span> <span style='color: white;'>Transportation</span>", unsafe_allow_html=True)
st.markdown("<span style='color: red;'>Skills take away From This Project:</span> <span style='color: white;'>Web Scraping using Selenium, Python, Streamlit, SQL</span>", unsafe_allow_html=True)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/848871b3-eeda-4854-9bc8-7616e2ffe678/f86GBVkM7M.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low")

#cd "/Users/sanjay/capstone1/capstone projects/capstone1 redbus/"
