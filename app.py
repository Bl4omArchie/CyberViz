from cyberviz.cyberframe import Cyberviz
from pathlib import Path

import streamlit as st
import tempfile


st.set_page_config(layout="wide")
st.title("📊 CyberViz Dataset Manager")


if "cvz" not in st.session_state:
    st.session_state["cvz"] = Cyberviz()

cyberviz = st.session_state["cvz"]


uploaded_file = st.file_uploader("📂 Upload a Dataset", type=["csv", "pcap", "parquet"])


if uploaded_file:
    tmp_path = Path(tempfile.gettempdir()) / uploaded_file.name
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        dsid = cyberviz.add_dataset(str(tmp_path))
        st.success(f"✅ Dataset loaded with ID: {dsid}")
    except Exception as e:
        st.error(f"❌ Failed to add dataset: {e}")


if cyberviz.datasets:
    st.subheader("📦 Datasets Loaded")
    for dsid, dataset in cyberviz.datasets.items():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"🔗 ID: `{dsid}`")
            st.write(f"📄 Name: {dataset.filename}")
            st.write(f"📐 Type: {type(dataset).__name__}")
        with col2:
            if st.button(f"Analyze {dsid}"):
                try:
                    cyberviz.activate_dataset([dsid])
                    cyberviz.analyze(dsid)
                    st.success(f"🧠 Analyzed {dsid}")
                except Exception as e:
                    st.error(f"❌ Error analyzing: {e}")
            if st.button(f"Remove {dsid}"):
                cyberviz.remove_dataset(dsid)
                st.experimental_rerun()
else:
    st.info("No datasets loaded yet.")
