from cyberviz.graphic import TreemapGraphic, Graphic
from cyberviz.core import Cyberviz
import streamlit as st

@st.cache_resource
def get_cyberviz() -> Cyberviz:
    return Cyberviz()


# Start Cyberviz framework
cyberviz = get_cyberviz()


# Set main page
st.set_page_config(layout="wide")
st.title("📊 Cyberviz Dashboard")

# Build Tabs
tabs = []
hash_to_name = {}

for hash, item in cyberviz.collection.index.items():
    name = item.name
    tabs.append(name)
    hash_to_name[name] = hash

tabs.append("➕ Upload")
selected_tab = st.tabs(tabs)

# Display content depending on selected tab
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

            new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_files]

            if new_files:
                for file in new_files:
                    cyberviz.load_dataset(file)
                    st.session_state.uploaded_files.add(file.name)
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

            # === Preview ===
            if preview_data is not None:
                with st.expander(f"🔍 Preview of {dataset.name}", expanded=True):
                    st.dataframe(preview_data)

                with st.expander(f"📊 Treemap Plot", expanded=True):
                    count = dataset.category("traffic_category").value_counts()
                    count_pd = count.compute()
                    total = count_pd.sum()
                    percent = count_pd / total

                    major_mask = percent >= 0.04
                    major_labels = count_pd[major_mask]
                    minor_labels = count_pd[~major_mask]

                    final_labels = []
                    final_sizes = []

                    for label, size in major_labels.items():
                        pct = size / total
                        final_labels.append(f"{label}\n{size} ({pct:.1%})")
                        final_sizes.append(size)

                    if not minor_labels.empty:
                        grouped_name = ', '.join(minor_labels.index.tolist())
                        grouped_label = f"Others\n({grouped_name})"
                        grouped_size = minor_labels.sum()
                        grouped_pct = grouped_size / total
                        grouped_label += f"\n{grouped_size} ({grouped_pct:.1%})"
                        final_labels.append(grouped_label)
                        final_sizes.append(grouped_size)

                    graph = Graphic.new_plot(
                        title="Traffic categories",
                        legend="Different traffic categories",
                        inputs=final_sizes,
                        labels=final_labels
                    )

                    obj = TreemapGraphic()
                    obj.plot_graph(graph)
