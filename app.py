import streamlit as st
from compressor import compress_image, compress_pdf, compress_text

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FileShrink | Universal Compressor", 
    page_icon="🗜️", 
    layout="centered",
    initial_sidebar_state="expanded" 
)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("📂 Navigation")
    mode = st.radio(
        "Select File Type:",
        ["Images", "PDFs", "Text & CSV"],
        index=0
    )
    
    st.divider()

    if mode == "Images":
        st.subheader("🖼️ Image Settings")
        img_quality = st.slider(
            "Compression Quality", 
            min_value=10, 
            max_value=90, 
            value=30, 
            help="Lower quality = smaller file size."
        )
    else:
        st.info(f"Settings for {mode} are optimized automatically.")
    
    st.divider()
    st.caption("v1.0.0 | Secure Offline Compression")

# --- 3. WELCOME DASHBOARD ---
def display_welcome(mode_name):
    st.subheader(f"Welcome to {mode_name} Compression")
    st.write("Optimize your digital footprint without compromising on privacy.")
    
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

# --- 4. CORE COMPRESSION LOGIC ---
def handle_compression(uploaded_file, category, quality=None):
    if uploaded_file is not None:
        orig_size_kb = uploaded_file.size / 1024
        
        # We use a spinner here instead of 'st.status' so it disappears completely
        with st.spinner(f"⚡ Shrinking {uploaded_file.name}..."):
            try:
                # Execution
                if category == "Image":
                    data, out_name, mime = compress_image(uploaded_file, quality=quality)
                elif category == "PDF":
                    data, out_name, mime = compress_pdf(uploaded_file)
                else:
                    data, out_name, mime = compress_text(uploaded_file)

                new_size_kb = len(data) / 1024
                reduction = (1 - (len(data) / uploaded_file.size)) * 100
                
                # --- EVERYTHING BELOW THIS APPEARS AUTOMATICALLY ---
                st.divider()
                st.success(f"🎉 **{uploaded_file.name}** is ready for download!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Original", f"{orig_size_kb:.1f} KB")
                m2.metric("New Size", f"{new_size_kb:.1f} KB", 
                         delta=f"-{orig_size_kb - new_size_kb:.1f} KB", 
                         delta_color="inverse")
                m3.metric("Reduction", f"{reduction:.1f}%")

                st.download_button(
                    label="📥 Download Compressed File",
                    data=data,
                    file_name=out_name,
                    mime=mime,
                    use_container_width=True,
                    type="primary"
                )
                
                if category == "Image":
                    with st.expander("👁️ View Preview", expanded=True):
                        st.image(data, use_container_width=True)
                        
            except Exception as e:
                st.error(f"❌ Compression failed: {e}")
    else:
        display_welcome(category)

# --- 5. MAIN CONTENT ---
st.title("FileShrink")

if mode == "Images":
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_up")
    handle_compression(img_file, "Image", quality=img_quality)

elif mode == "PDFs":
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_up")
    handle_compression(pdf_file, "PDF")

elif mode == "Text & CSV":
    txt_file = st.file_uploader("Upload Text/CSV", type=["txt", "csv"], key="txt_up")
    handle_compression(txt_file, "Document")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Secure, browser-side processing. Built with Streamlit.")