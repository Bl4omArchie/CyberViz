from cyberviz.core import Cyberviz

import streamlit as st


@st.cache_resource
def get_cyberviz() -> Cyberviz:
    return Cyberviz()


cyberviz = get_cyberviz()

st.set_page_config(layout="wide")
st.sidebar.title("📂 Upload Datasets")

uploaded_files = st.sidebar.file_uploader("Upload files (max 2GB)", type=["csv", "pcap"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        cyberviz.load_dataset(file)

st.sidebar.markdown("---")
st.sidebar.subheader("📄 Datasets")

for hash, item in cyberviz.collection.index.items():
    file_name = item.name

    cols = st.sidebar.columns([6, 1])
    with cols[0]:
        if st.button(file_name, key=hash):
            cyberviz.activate(hash)
            st.session_state["active_hash"] = hash

    with cols[1]:
        if st.button("🗑️", key=f"delete_{hash}"):
            cyberviz.delete(hash)

            if st.session_state.get("active_hash") == hash:
                del st.session_state["active_hash"]

            st.rerun()

if "active_hash" in st.session_state:
    active_hash = st.session_state["active_hash"]
    preview_data = cyberviz.get_preview(active_hash)
    dataset = cyberviz.collection.index[active_hash]

    if preview_data is not None:
        with st.expander(f"🔍 Preview of {dataset.name}", expanded=True):
            st.dataframe(preview_data)

    # Metadata display below preview
    with st.expander(f"ℹ️ Metadata for {dataset.name}", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**📛 Name:** `{dataset.name}`")
            st.markdown(f"**🔢 Hash:** `{active_hash}`")
            st.markdown(f"**🗃️ Extension:** `{dataset.extension}`")
            st.markdown(f"**📦 Size:** `{dataset.size} MB`")
