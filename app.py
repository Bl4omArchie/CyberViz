from cyberviz.cyberframe import Cyberviz, CsvFormat, ParquetFormat, PcapFormat
from pathlib import Path
import streamlit as st
import tempfile
import dask.dataframe as dd

st.set_page_config(layout="wide")
st.title("📊 CyberViz Dataset Manager")

# Initialize or retrieve the Cyberviz instance in session_state
if "cvz" not in st.session_state:
    st.session_state["cvz"] = Cyberviz()
cyberviz = st.session_state["cvz"]

# Upload widget in sidebar
with st.sidebar:
    st.header("📂 Upload Dataset")
    uploaded_file = st.file_uploader("", type=["csv", "pcap", "parquet"])

if uploaded_file:
    tmp_path = Path(tempfile.gettempdir()) / uploaded_file.name
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.read())

    cyberviz.add_dataset(str(tmp_path))
    st.sidebar.success(f"✅ Dataset loaded with ID: {list(cyberviz.datasets.keys())[-1]}")


# Show loaded datasets in main area
if cyberviz.datasets:
    st.subheader("📦 Datasets Loaded")
    for dsid, dataset in cyberviz.datasets.items():
        with st.container():
            st.markdown("---")
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"#### 📄 {dataset.name}")
                st.write(f"- **ID**: `{dsid}`")
                st.write(f"- **Type**: `{dataset.extension}`")
                st.write(f"- **Size**: {dataset.size:.2f} MB")
                st.write(f"- **Path**: `{dataset.path}`")

            with col2:
                preview_key = f"preview_{dsid}"
                analyze_key = f"analyze_{dsid}"
                remove_key = f"remove_{dsid}"

                if st.button("👁️ Preview", key=preview_key):
                    try:
                        cyberviz.activate([dsid])
                        st.session_state["preview_dataset"] = dsid
                    except Exception as e:
                        st.error(f"❌ Error activating: {e}")

                if st.button("🧠 Analyze", key=analyze_key):
                    try:
                        cyberviz.activate([dsid])
                        st.success(f"🧠 Analyzed {dsid}")
                    except Exception as e:
                        st.error(f"❌ Error analyzing: {e}")

                if st.button("🗑️ Remove", key=remove_key):
                    try:
                        cyberviz.deactivate([dsid])
                        del cyberviz.datasets[dsid]
                        if "preview_dataset" in st.session_state and st.session_state["preview_dataset"] == dsid:
                            del st.session_state["preview_dataset"]
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"❌ Error removing dataset: {e}")

    # Show preview modal if requested
    if "preview_dataset" in st.session_state:
        dsid = st.session_state["preview_dataset"]
        try:
            dataset_obj = cyberviz.activate_dataset[dsid]
            st.markdown("---")
            st.subheader(f"👁️ Preview of `{dsid}`")

            if isinstance(dataset_obj, CsvFormat):
                df = dd.read_csv(dataset_obj.dataset.path, blocksize="1MB").compute()
                st.dataframe(df.head(20))

            elif isinstance(dataset_obj, ParquetFormat):
                df = dd.read_parquet(dataset_obj.dataset.path).compute()
                st.dataframe(df.head(20))

            elif isinstance(dataset_obj, PcapFormat):
                st.warning("PCAP preview not yet implemented.")

        except Exception as e:
            st.error(f"❌ Failed to load preview: {e}")

else:
    st.info("No datasets loaded yet.")
