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
    st.title(" Navigation")
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
            help="Lower quality = smaller file size. 30 is recommended."
        )
    else:
        st.info(f"Settings for {mode} are optimized automatically.")
    
    st.divider()
    st.caption("v1.0.0 | Secure Offline Compression")

# --- 3. REUSABLE UI COMPONENTS ---
def display_welcome(mode_name):
    """Fills the empty space with feature cards when no file is uploaded."""
    st.subheader(f"Welcome to {mode_name} Compression")
    st.write("Optimize your digital footprint without compromising on privacy.")
    
    # Feature Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔒 Private")
        st.caption("Files never leave your browser.")
    with col2:
        st.markdown("### ⚡ Fast")
        st.caption("Instant processing on your device.")
    with col3:
        st.markdown("### 📉 High Ratio")
        st.caption("Advanced data reduction logic.")
    st.divider()

def handle_compression(uploaded_file, category, quality=None):
    if uploaded_file is not None:
        orig_size_kb = uploaded_file.size / 1024
        st.write(f"📂 **Selected File:** `{uploaded_file.name}` ({orig_size_kb:.2f} KB)")
        
        if st.button(f"🚀 Start {category} Compression", use_container_width=True, type="primary"):
            with st.status("Compressing...", expanded=True) as status:
                try:
                    if category == "Image":
                        data, out_name, mime = compress_image(uploaded_file, quality=quality)
                    elif category == "PDF":
                        data, out_name, mime = compress_pdf(uploaded_file)
                    else:
                        data, out_name, mime = compress_text(uploaded_file)

                    new_size_kb = len(data) / 1024
                    reduction = (1 - (len(data) / uploaded_file.size)) * 100
                    
                    status.update(label="Success!", state="complete", expanded=False)
                    
                    # Result Section
                    st.divider()
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Original", f"{orig_size_kb:.1f} KB")
                    m2.metric("New Size", f"{new_size_kb:.1f} KB", delta=f"-{orig_size_kb - new_size_kb:.1f} KB", delta_color="inverse")
                    m3.metric("Saved", f"{reduction:.1f}%")

                    st.download_button(
                        label="📥 Download Compressed File",
                        data=data,
                        file_name=out_name,
                        mime=mime,
                        use_container_width=True
                    )
                    
                    if category == "Image":
                        with st.expander("👁️ View Preview"):
                            st.image(data, use_container_width=True)
                            
                except Exception as e:
                    status.update(label="Failed", state="error")
                    st.error(f"Error: {e}")
    else:
        display_welcome(category)

# --- 4. MAIN APP CONTENT ---
st.title("📂 FileShrink")

if mode == "Images":
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_up")
    handle_compression(img_file, "Image", quality=img_quality)

elif mode == "PDFs":
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_up")
    handle_compression(pdf_file, "PDF")

elif mode == "Text & CSV":
    txt_file = st.file_uploader("Upload Text/CSV", type=["txt", "csv"], key="txt_up")
    handle_compression(txt_file, "Document")

# --- 5. FOOTER ---
st.caption("Secure, browser-side processing. Built with Streamlit.")