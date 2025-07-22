from cyberviz.core import Cyberviz

import streamlit as st


st.set_page_config(layout="wide")
st.title("📊 CyberViz Dataset Manager")


if "cvz" not in st.session_state:
    st.session_state["cvz"] = Cyberviz()
cyberviz = st.session_state["cvz"]


with st.sidebar:
    st.header("📂 Upload Dataset")
    uploaded_file = st.file_uploader("", type=["csv", "pcap", "parquet"])


if uploaded_file:
    if cyberviz.load_dataset(uploaded_file):
        st.sidebar.success(f"✅ Dataset loaded with ID: {list(cyberviz.collection.index.keys())[-1]}")
    else:
        st.sidebar.error(f"✅ Dataset couldn't be loaded.")


if cyberviz.collection.index:
    st.subheader("📦 Datasets Loaded")
    for dhash, dataset in list(cyberviz.collection.index.items()):
        with st.container():
            st.markdown("---")
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"#### 📄 {dataset.name}")
                st.write(f"- **ID**: `{dhash}`")
                st.write(f"- **Type**: `{dataset.extension}`")
                st.write(f"- **Size**: {dataset.size:.2f} MB")
                st.write(f"- **Path**: `{dataset.path}`")

            with col2:
                preview_key = f"preview_{dhash}"
                analyze_key = f"analyze_{dhash}"
                remove_key = f"remove_{dhash}"

                if st.button("👁️ Preview", key=preview_key):
                    cyberviz.activate(dhash)
                    st.session_state["preview_dataset"] = dhash

                if st.button("🧠 Analyze", key=analyze_key):
                    st.error(f"❌ Not implemented yet")

                if st.button("🗑️ Remove", key=remove_key):
                    try:
                        cyberviz.delete(dhash)
                        if st.session_state.get("preview_dataset") == dhash:
                            del st.session_state["preview_dataset"]
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error removing dataset: {e}")


else:
    st.info("No datasets loaded yet.")
