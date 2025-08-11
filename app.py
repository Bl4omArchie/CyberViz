from cyberviz.graphic import new_graph
from cyberviz.core import Cyberviz
import streamlit as st


@st.cache_resource
def get_cyberviz() -> Cyberviz:
    return Cyberviz()


# Start Cyberviz framework
cyberviz = get_cyberviz()

st.set_page_config(layout="wide")
st.title("📊 Cyberviz Dashboard")

tabs = []
hash_to_name = {}

for hash, item in cyberviz.collection.index.items():
    name = item.name
    tabs.append(name)
    hash_to_name[name] = hash

tabs.append("➕ Upload")
selected_tab = st.tabs(tabs)


for i, tab in enumerate(selected_tab):
    with tab:
        tab_name = tabs[i]
        if tab_name == "➕ Upload":
            st.subheader("📂 Upload New Datasets")
            uploaded_files = st.file_uploader(
                "Drag and drop files here (max 2GB)", type=["csv", "pcap"],
                accept_multiple_files=True, label_visibility="collapsed"
            )

            if 'uploaded_files' not in st.session_state:
                st.session_state.uploaded_files = set()

            new_datasets = [f for f in uploaded_files if f.name not in st.session_state.uploaded_files]

            if new_datasets:
                for dataset in new_datasets:
                    cyberviz.load_dataset(dataset)
                    st.session_state.uploaded_files.add(dataset.name)
                    new_datasets = []

                st.success("✅ Uploaded successfully.")
                st.rerun()


        elif tab_name in hash_to_name:
            active_hash = hash_to_name[tab_name]
            active_hash = hash_to_name[tabs[i]]
            dataset = cyberviz.collection.index[active_hash]
            preview_data = cyberviz.get_preview(active_hash)

            st.subheader(f"📄 Dataset: `{dataset.name}`")

            col1, col2 = st.columns([6, 1])
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{active_hash}"):
                    cyberviz.delete(active_hash)
                    st.rerun()

            # === Metadata ===
            with st.expander(f"ℹ️ Metadata for {dataset.name}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📛 Name:** `{dataset.name}`")
                    st.markdown(f"**🔢 Hash:** `{active_hash}`")
                    st.markdown(f"**🗃️ Extension:** `{dataset.extension}`")
                    st.markdown(f"**📦 Size:** `{dataset.size} MB`")

            if preview_data is not None:
                with st.expander(f"🔍 Preview of {dataset.name}", expanded=True):
                    st.dataframe(preview_data)

                with st.expander("📈 Visualize Column Data", expanded=True):
                    col_names = dataset.content.columns

                    chart_type = st.radio("Choose a chart type", ["Treemap", "Pie Chart", "Histogram"], horizontal=True)
                    selected_col = st.selectbox("Select column to visualize", col_names)

                    if selected_col:
                        series = dataset.category(selected_col)
                        value_counts = series.value_counts().compute()
                        labels = [f"{idx} ({val})" for idx, val in value_counts.items()]
                        values = value_counts.tolist()
                        
                        obj = new_graph(
                            graph_type=chart_type,
                            title=f"{chart_type} of {selected_col}",
                            legend=f"Distribution of {selected_col}",
                            inputs=values,
                            labels=labels
                        )

                        if obj:
                            obj.plot_graph()
