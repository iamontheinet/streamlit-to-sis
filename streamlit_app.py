# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setup web page
st.set_page_config(
     page_title="Unsupported SiS features",
     layout="wide",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "The source code for this application can be accessed on GitHub https://github.com/iamontheinet/streamlit-to-sis"
     }
)

docs_url = 'https://docs.snowflake.com/en/LIMITEDACCESS/streamlit-in-snowflake#unsupported-streamlit-features'

def unsupported_features(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    features = soup.find_all("a", {"class": "reference external"})
    features = [f.text for f in features if f.text.startswith('st.')]

    others = soup.find("div", {"id":"limitations-when-using-streamlit-in-snowflake"}).find_all("div")
    others = [o.find('h3').text[:-1] for o in others]
    return features,others

st.header(f"Currently unsupported features in Streamlit-In-Snowflake (SiS)")
st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
st.markdown("___")

st.subheader("Upload your Streamlit Python app file to see which features are currently *not* supported in SiS")
uploaded_file = st.file_uploader("Upload your Streamlit Python file", accept_multiple_files=False, label_visibility='hidden')
if uploaded_file is not None:
    features,others = unsupported_features(docs_url)
    code_lines = uploaded_file.getvalue().decode('utf-8').splitlines()

    with st.container():
        data = []
        for code_line in code_lines:
            for f in features:
                idx = code_line.find(f)
                if idx > 0:
                    data.append([f,code_line.strip()])

        df = pd.DataFrame(data,columns=['Unsupported Feature in SiS','Line'])
        st.dataframe(df, use_container_width=True)

        st.markdown("___")

        st.subheader("Other Limitations")
        for o in others:
            st.text("* " + o)
