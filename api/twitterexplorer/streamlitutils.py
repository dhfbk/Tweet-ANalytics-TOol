## =============================================================================
## twitter explorer 
## streamlit-related functions
## =============================================================================

from twitterexplorer.config import version_number
import streamlit as st
import os

def ui_changes():
    st.markdown('<link rel="preconnect" href="https://fonts.googleapis.com">\
                 <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\
                 <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet"> ',
                unsafe_allow_html=True)
    st.markdown(
        '<style> \
        body{font-family:"Inter", -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica\
         Neue",Arial,sans-serif} \
        p{font-family:"Inter", -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica\
         Neue",Arial,sans-serif} \
        h1,h2,h3{font-family:\
        "Inter", -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica\
         Neue",Arial,sans-serif} \
         .css-1ekf893{font-family:\
        "Inter", -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica\
         Neue",Arial,sans-serif}\
        .reportview-container .markdown-text-container{font-family:\
        "Inter", -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica\
         Neue",Arial,sans-serif} \
         #titlelink {color: white;\
         text-decoration: none;\
         font-family:""Inter", -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica\
         Neue",Arial,sans-serif;\
         margin-bottom:0} \
         #titlelink:hover {color: #e56a69;\
         text-decoration: none} \
         .css-qrbaxs{font-size:10pt} \
         code{color:black} \
         .css-1ekf893 a{color:#000} \
         .reportview-container .markdown-text-container a{color:rgba(83,106,160,1)} \
         .css-1ekf893 a:hover{color:#eee;} \
         .st-ae{font-family:"Inter",-apple-system,system-ui,BlinkMacSystemFont,\
                "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:10pt} \
         </style>', unsafe_allow_html=True)
    st.markdown('<head><title>redStand By Me</title></head>',
                unsafe_allow_html=True)
    st.markdown(f'<p style="font-size: 40pt; font-weight: bold; color: black; \
        background-color: #e56a69">&nbsp;\
        <a id="titlelink" href="https://www.standbymeproject.eu/standbyme-2-0/">Tweet ANalytics TOol (TANTO)\
        <span style="font-size:10pt;"></span></a>\
        </p>', unsafe_allow_html=True)

def file_selector(folder_path='.'):
    try:
        filenames = os.listdir(folder_path)
    except FileNotFoundError:
        st.error("The `./data` folder does not exist. Please create it and insert \
                your Twitter collections.")
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')
    filenames = list(reversed(sorted(filenames)))
    filenames.insert(0,'---')
    selected_filename = st.selectbox(
        'Select a tweet collection', 
        filenames,
        help='The function that loads the data uses @st.cache to speed up \
              repeated loading of the same dataset. If your dataset has changed\
              in between two runs but the filename is the same, please clear\
              the cache by pressing C.')
    return os.path.join(folder_path, selected_filename)
