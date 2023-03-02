# Import the necessary libraries
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

# Setup web page
st.set_page_config(
    page_title="Unsupported SiS features",
    layout="wide",
    menu_items={
        "Get Help": "https://developers.snowflake.com",
        "About": "The source code for this application can be accessed on GitHub https://github.com/iamontheinet/streamlit-to-sis",
    },
)

docs_url = "https://docs.snowflake.com/en/LIMITEDACCESS/streamlit-in-snowflake#unsupported-streamlit-features"

def unsupported_features(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    features = soup.find_all("a", {"class": "reference external"})
    features = [f.text for f in features if f.text.startswith("st.")]
    features = features + [f.replace("st.", "st.sidebar.") for f in features]
    possible_features = features + [f.replace("st.", ".") for f in features]

    others = soup.find("div", {"id": "limitations-when-using-streamlit-in-snowflake"}).find_all(
        "div"
    )
    others = [o.find("h3").text[:-1] for o in others]
    return features, possible_features, others

def check_valid_github_url(url):
    if "github" in url and ("blob" in url or "raw" in url):
        return True

st.header(f"Currently unsupported features in Streamlit-In-Snowflake (SiS)")
st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
st.markdown("___")

with st.container():
    col1,col2= st.columns(2, gap='large')

    with col1:
        st.subheader(
            "Upload your Streamlit Python app file, OR 👉"
        )
        uploaded_file = st.file_uploader(
            "Upload your Streamlit Python file", accept_multiple_files=False, label_visibility="hidden"
        )

    # with col2:
    #     st.subheader("OR")
    
    with col2:
        st.subheader("Provide the GitHub URL of your Streamlit app Python file")
        st.text("For example, https://github.com/iamontheinet/streamlit-to-sis/blob/main/streamlit_app.py")
        streamlit_link = st.text_input(
            "Enter the GitHub URL of your Streamlit app Python file",
            label_visibility="hidden"
        )

if uploaded_file is not None or check_valid_github_url(streamlit_link):
    features, possible_features, others = unsupported_features(docs_url)
    if uploaded_file is not None:
        code_lines = uploaded_file.getvalue().decode("utf-8").splitlines()
    elif check_valid_github_url(streamlit_link):
        streamlit_link = streamlit_link.replace("blob", "raw")
        response = requests.get(streamlit_link)
        code_lines = response.text.splitlines()

    if code_lines:
        with st.container():
            data = []
            possible_bad_features = []
            for code_line in code_lines:
                for f in features:
                    idx = code_line.find(f)
                    if idx > 0:
                        data.append([f, code_line.strip()])
                for p in possible_features:
                    idx = code_line.find(p)
                    if idx > 0:
                        possible_bad_features.append([p, code_line.strip()])

            df = pd.DataFrame(data, columns=["Unsupported Feature in SiS", "Line"])
            pbf = pd.DataFrame(
                possible_bad_features, columns=["Possibly Unsupported Feature in SiS", "Line"]
            )

            # Remove any lines from pbf where the Line is in df
            pbf = pbf[~pbf["Line"].isin(df["Line"])]

            st.subheader("Unsupported Features")
            st.dataframe(df, use_container_width=True)

            st.markdown("___")
            st.subheader("Possible Unsupported Features")
            st.dataframe(pbf, use_container_width=True)

            st.markdown("___")

            st.subheader("Other Limitations")
            for o in others:
                st.text("* " + o)
    else:
        st.write("Please upload a Streamlit Python file or provide a GitHub URL for it.")
