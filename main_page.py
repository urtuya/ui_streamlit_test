import streamlit as st

import os
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

def web_introductory_text():
    """
        Introduction and usage text
    """

    st.sidebar.title("General info")
    st.sidebar.info(
        """
        - TODO
        - add confluence
        - add github
        - add credentials (?)
        """
    )

    st.title("Streamlit demo")
    st.image("imgs/cat.jpg", caption="Intro cat")
    st.divider()

    st.header("Some headers for short description")
    st.subheader("Usage")
    st.markdown(
        """
            How to use:
            1. Upload a dataset in .csv format
            2. Upload audio file in .mp3 format
            3. Download the result (.txt without diarization, excel for diarization)
        """
    )

    st.button("Refresh page", on_click=st.rerun)
    st.divider()


def save_uploadedfile(uploadedfile, flag_show):
    with open(os.path.join('downloaded_files/', uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

    if flag_show:
        data = pd.read_csv(os.path.join('downloaded_files/', uploadedfile.name))
        st.text(uploadedfile.name)
        st.dataframe(data)


def show_dataframe(path_to_file):
    data = pd.read_csv(os.path.join('downloaded_files/', path_to_file))
    st.dataframe(data)


def show_graph():
    df = pd.read_csv("downloaded_files/reviews.csv")
    df['text_len'] = df['Text'].apply(len)

    fig = px.histogram(
        df,
        x='text_len',
        range_x=[0, 4000],
        title="text len distribution"
    )

    st.plotly_chart(fig, use_container_width=True)



if __name__ == "__main__":

    st.sidebar.markdown("# Main page")
    if not os.path.exists("downloaded_files"):
        os.makedirs("downloaded_files")



    ### 1. Intro
    web_introductory_text()

    ### 2. CSV: Upload files + download locally
    st.subheader("Download CSV files")

    flag_showtable = st.toggle("Show table") ## сделать виджет вместо галочки
    uploaded_files = st.file_uploader("Choose a CSV file",
                                      accept_multiple_files=True,
                                      type=["csv"],
                                      key="uploading_csv"
                                      )
    uploaded_filenames = [file.name for file in uploaded_files]
    for uploaded_file in uploaded_files:
        save_uploadedfile(uploaded_file, flag_show=flag_showtable)
    
    st.divider()


    ### 3. Show tables by choose
    
    buttons_list = []
    for i in range(len(uploaded_filenames)):
        buttons_list.append(st.button("Show " + uploaded_filenames[i]))

    for i in range(len(buttons_list)):
        if buttons_list[i]:
            dataframe = pd.read_csv(os.path.join('downloaded_files/', uploaded_filenames[i]))
            st.dataframe(dataframe)

    st.divider()

    ### 3.1 Radio
    st.header("Choose options by toggle")
    choice = st.radio("Number of options == number of downloaded files",
             uploaded_filenames)
    if choice:
        st.text("Your choice: " + choice)
    
    st.divider()

    ### 3.2 Selectbox
    st.header("Choose options by selectbox")
    option = st.selectbox("Choose one option", set(uploaded_filenames))
    if option:
        st.text("Your option: " + option)

    st.divider()

    ### 3.3 Multiselect
    st.header("Multiselect")
    options = st.multiselect("Choose one or more options", uploaded_filenames)

    if options:
        for i in options:
            st.text("Your option: " + i)
    st.divider()


    ### 4. Graphics

    agree = st.checkbox("Show graphics")
    if agree:
        show_graph()
