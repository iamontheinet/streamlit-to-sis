# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

APP_ICON_URL = "snowpark-icon.png"

# Setup web page
st.set_page_config(
     page_title="Unsupported SiS features",
     page_icon=APP_ICON_URL,
     layout="wide",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "The source code for this application can be accessed on GitHub https://github.com/iamontheinet/snowpark-python-anaconda"
     }
)

st.markdown("""
    <style type="text/css">
    blockquote {
        margin: 1em 0px 1em -1px;
        padding: 0px 0px 0px 1.2em;
        font-size: 20px;
        border-left: 5px solid rgb(230, 234, 241);
        # background-color: rgb(129, 164, 182);
    }
    blockquote p {
        font-size: 30px;
        color: #FFFFFF;
    }
    [data-testid=stSidebar] {
        background-color: rgb(129, 164, 182);
        color: #FFFFFF;
    }
    [aria-selected="true"] {
         color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

docs_url = 'https://docs.snowflake.com/en/LIMITEDACCESS/streamlit-in-snowflake#unsupported-streamlit-features'

def unsupported_features(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    features = soup.find_all("a", {"class": "reference external"})
    features = [f.text for f in features if f.text.startswith('st.')]
    return features

st.title(f"List of currently unsupported features in Streamlit-In-Snowflake (SiS)")
st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
st.markdown("___")

st.subheader("Upload your Streamlit Python app file to see what will not work in SiS")
uploaded_file = st.file_uploader("Upload your Streamlit Python file", accept_multiple_files=False, label_visibility='hidden')
if uploaded_file is not None:
    features = unsupported_features(docs_url)
    code_lines = uploaded_file.getvalue().decode('utf-8').splitlines()

    st.markdown("___")

    with st.container():
        st.caption(f"List of currently unsupported features in SiS")
        data = []
        for code_line in code_lines:
            for f in features:
                idx = code_line.find(f)
                if idx > 0:
                    data.append([f,code_line.strip()])

        df = pd.DataFrame(data,columns=['Feature','Line'])
        st.dataframe(df, use_container_width=True)
