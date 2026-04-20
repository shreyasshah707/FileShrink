import streamlit as st
import compressor as comp

st.set_page_config(page_title="FileShrink", page_icon="🗜️", layout="centered", initial_sidebar_state="expanded")

# --- SIDEBAR ---
with st.sidebar:
    st.title("📂 Navigation")
    mode = st.radio("File Type:", ["Images", "PDFs", "Text Files", "CSVs"])
    if mode == "Images":
        quality = st.slider("Quality", 10, 90, 30)
    st.divider()

# --- WELCOME UI ---
def welcome(name):
    st.subheader(f"Welcome to {name} Optimizer")
    st.write("Upload your files to our cloud-powered engine for instant optimization.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### ☁️ Cloud")
        st.caption("Powered by Streamlit Cloud.")
    with c2:
        st.markdown("### ⚡ Fast")
        st.caption("High-speed server processing.")
    with c3:
        st.markdown("### 📉 Analysis")
        st.caption("Deep algorithm insights.")
    st.divider()

# --- MAIN LOGIC ---
st.title("FileShrink")

if mode == "Images":
    f = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if f:
        with st.spinner("Processing..."):
            data, name, mime = comp.compress_image(f, quality)
            st.success("Compressed!")
            st.download_button("📥 Download", data, name, mime, use_container_width=True, type="primary")
            st.image(data)
    else: welcome(mode)

elif mode == "PDFs":
    f = st.file_uploader("Upload PDF", type=["pdf"])
    if f:
        with st.spinner("Processing..."):
            data, name, mime = comp.compress_pdf(f)
            st.success("Optimized!")
            st.download_button("📥 Download", data, name, mime, use_container_width=True, type="primary")
    else: welcome(mode)

elif mode == "Text Files":
    f = st.file_uploader("Upload Text", type=["txt"])
    if f:
        with st.spinner("⚡ Running Merge Sort Analysis..."):
            data, name, mime, stats = comp.analyze_and_compress_txt(f)
            st.write("### 📊 Custom Analysis")
            m1, m2, m3 = st.columns(3)
            m1.metric("Original", f"{stats['total_chars']} B")
            m2.metric("Projected", f"{stats['projected_size']} B", delta=f"-{stats['expected_ratio']:.1f}%")
            m3.metric("Avg Word", f"{stats['avg_len']:.1f}")
            with st.expander("🔍 Top 10 Frequencies (Merge Sorted)", expanded=True):
                for w, fr in stats['top_words']: st.write(f"**{w}**: {fr}")
            st.download_button("📥 Download ZIP", data, name, mime, use_container_width=True, type="primary")
    else: welcome(mode)

elif mode == "CSVs":
    f = st.file_uploader("Upload CSV", type=["csv"])
    if f:
        with st.spinner("Zipping..."):
            data, name, mime = comp.compress_csv(f)
            st.success("CSV Compressed")
            st.download_button("📥 Download", data, name, mime, use_container_width=True, type="primary")
    else: welcome(mode)