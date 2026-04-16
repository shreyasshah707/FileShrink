# 🌀 FileShrink: Universal File Compressor

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)

**FileShrink** is a high-performance web tool built with Streamlit that reduces the footprint of your digital life. Featuring a modern Neomorphic UI, it handles Images, PDFs, and Text files with specialized compression algorithms.

## 🚀 Features
- **🖼️ Image Optimization:** Lossy JPEG compression via Pillow (Quality: 30).
- **📄 PDF Stream Compression:** Internal content stream optimization via PyPDF2.
- **🗜️ Archive Compression:** Deflate-based ZIP archiving for TXT and CSV files.
- **🎨 Neomorphic UI:** Soft-UI aesthetics with full light/dark mode support.

## 🛠️ Installation & Usage
1. Clone the repo: `git clone https://github.com/shreyasshah707/FileShrink.git`
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## 📂 Project Structure
- `app.py`: Streamlit frontend and UI styling.
- `compressor.py`: Core compression logic and processing.