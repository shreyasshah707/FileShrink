# 🗜️ FileShrink | Universal File Compressor

FileShrink is a high-performance, secure, browser-based file optimization tool. It allows users to compress Images, PDFs, and Text files using a combination of standard libraries and custom-built algorithms.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

## 🚀 Features

- **🖼️ Image Optimization:** Uses lossy compression logic to reduce JPEG/PNG sizes by up to 80% while maintaining visual clarity.
- **📄 PDF Structural Compression:** Optimizes internal content streams and removes redundant structures within PDF documents.
- **📊 Text Analysis & ZIP:** A deep-dive compression module that analyzes word frequencies and calculates theoretical compression ratios.
- **🔒 Privacy First:** All processing happens in-memory within your browser. No files are ever uploaded to a server or stored permanently.

## 🧠 Technical Implementation

This project was built to demonstrate core Computer Science fundamentals:

### 1. Custom Merge Sort
The Text & CSV module utilizes a manual implementation of the **Merge Sort** algorithm to sort word frequencies. This ensures an $O(n \log n)$ time complexity for dictionary generation, making it efficient even for larger text files.



### 2. Data Analysis with NumPy
We utilize **NumPy** to process text data at scale, specifically:
- Converting word lengths into multi-dimensional arrays.
- Calculating statistical means of word distributions to determine file "density."

### 3. Expected Compression Ratio
The app calculates a "Theoretical Dictionary Compression" value. This logic simulates how **Huffman Coding** works by identifying the top 10 most frequent words and calculating the bytes saved if replaced by 1-byte pointers.



## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shreyasshah707/FileShrink.git](https://github.com/shreyasshah707/FileShrink.git)
   cd FileShrink