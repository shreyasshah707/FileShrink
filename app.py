import streamlit as st
from compressor import compress_image, compress_pdf, compress_text_with_analysis

st.set_page_config(
    page_title="FileShrink", 
    page_icon="🗜️", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("📂 Navigation")
    mode = st.radio("Select File Type:", ["Images", "PDFs", "Text & CSV"], index=0)
    st.divider()
    if mode == "Images":
        st.subheader("🖼️ Image Settings")
        img_quality = st.slider("Quality", 10, 90, 30)
    else:
        st.info(f"Settings for {mode} are optimized automatically.")
    st.divider()
    st.caption("v1.2 | Custom Logic Edition")

def display_welcome(mode_name):
    st.subheader(f"Welcome to {mode_name} Compression")
    st.write("Optimize your files with our secure, on-device processing.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔒 Private")
        st.caption("Files never leave your browser.")
    with col2:
        st.markdown("### ⚡ Fast")
        st.caption("Instant local processing.")
    with col3:
        st.markdown("### 📉 Smart")
        st.caption("Maintains essential quality.")
    st.divider()

st.title("FileShrink")

if mode == "Images":
    f = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_up")
    if f:
        with st.spinner("⚡ Shrinking Image..."):
            data, name, mime = compress_image(f, img_quality)
            st.divider()
            st.success(f"**{f.name}** is ready!")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Original", f"{f.size/1024:.1f} KB")
            m2.metric("New Size", f"{len(data)/1024:.1f} KB", delta=f"-{(f.size - len(data))/1024:.1f} KB", delta_color="inverse")
            st.download_button("📥 Download", data, name, mime, use_container_width=True, type="primary")
            with st.expander("👁️ View Preview", expanded=True):
                st.image(data, use_container_width=True)
    else:
        display_welcome(mode)

elif mode == "PDFs":
    f = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_up")
    if f:
        with st.spinner("⚡ Shrinking PDF..."):
            data, name, mime = compress_pdf(f)
            st.divider()
            st.success("PDF Compression Complete!")
            m1, m2 = st.columns(2)
            m1.metric("Original", f"{f.size/1024:.1f} KB")
            m2.metric("New Size", f"{len(data)/1024:.1f} KB", delta_color="inverse")
            st.download_button("📥 Download", data, name, mime, use_container_width=True, type="primary")
    else:
        display_welcome(mode)

elif mode == "Text & CSV":
    f = st.file_uploader("Upload Text/CSV", type=["txt", "csv"], key="txt_up")
    if f:
        with st.spinner("⚡ Analyzing & Compressing..."):
            data, name, mime, stats = compress_text_with_analysis(f)
            st.divider()
            st.write("### 📊 Compression Analysis")
            m1, m2, m3 = st.columns(3)
            m1.metric("Current", f"{stats['total_chars']} B")
            m2.metric("Projected", f"{stats['projected_size']} B", delta=f"-{stats['expected_ratio']:.1f}%")
            m3.metric("Avg Word", f"{stats['avg_len']:.1f}")

            with st.expander("🔍 Top 10 Frequency Dictionary (Merge Sorted)", expanded=True):
                for word, freq in stats['top_words']:
                    st.write(f"**{word}**: {freq} occurrences")

            st.download_button("📥 Download ZIP", data, name, mime, use_container_width=True, type="primary")
    else:
        display_welcome(mode)

st.markdown("---")
st.caption("Secure, browser-side processing. Built with Streamlit.")