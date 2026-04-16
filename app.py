import streamlit as st
# Updated imports to reflect the changes in compressor.py
from compressor import compress_image, compress_pdf, compress_text

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="FileShrink", page_icon="🗜️", layout="centered")

st.title("🗜️ FileShrink")
st.write("Compress your Images, PDFs, and Text/CSV files easily and securely in your browser!")

# --- MAIN APP LOGIC ---
uploaded_file = st.file_uploader("Upload a file to compress", type=["png", "jpg", "jpeg", "pdf", "txt", "csv"])

if uploaded_file is not None:
    # Get file details
    file_extension = uploaded_file.name.split('.')[-1].lower()
    original_size = uploaded_file.size
    
    st.write(f"**Original File Size:** {original_size / 1024:.2f} KB")
    
    if st.button("Compress File"):
        with st.spinner('Compressing... Please wait.'):
            try:
                compressed_data = None
                download_name = ""
                mime_type = ""
                
                # Route to the correct logic based on file type
                if file_extension in ['jpg', 'jpeg', 'png']:
                    compressed_data, download_name, mime_type = compress_image(uploaded_file)
                    
                elif file_extension == 'pdf':
                    compressed_data, download_name, mime_type = compress_pdf(uploaded_file)
                    
                elif file_extension in ['txt', 'csv']:
                    compressed_data, download_name, mime_type = compress_text(uploaded_file)
                
                # Calculate new size and display success
                new_size = len(compressed_data)
                st.success("File processed successfully!")
                
                # Show before/after metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Original Size", f"{original_size / 1024:.2f} KB")
                col2.metric("New Size", f"{new_size / 1024:.2f} KB")
                
                reduction = (1 - (new_size / original_size)) * 100
                col3.metric("Reduction", f"{reduction:.1f}%")
                
                # Provide the download button
                st.download_button(
                    label=f"⬇️ Download {download_name}",
                    data=compressed_data,
                    file_name=download_name,
                    mime=mime_type,
                    type="primary"
                )
                
            except Exception as e:
                st.error(f"An error occurred during compression: {e}")