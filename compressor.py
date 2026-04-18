import io
import os
import zipfile
import numpy as np
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

#Merge sort
def merge_sort(items):
    if len(items) <= 1:
        return items
    
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0][1] >= right[0][1]: # Sort by count 
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result

#Image compression
def compress_image(uploaded_file, quality=30):
    img = Image.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    out = io.BytesIO()
    img.save(out, format="JPEG", quality=quality, optimize=True)
    return out.getvalue(), f"shrunk_{os.path.splitext(uploaded_file.name)[0]}.jpg", "image/jpeg"

#PDF compression
def compress_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    
    out = io.BytesIO()
    writer.write(out)
    return out.getvalue(), f"shrunk_{uploaded_file.name}", "application/pdf"

# txt analysis and compression
def compress_text_with_analysis(uploaded_file):
    raw_data = uploaded_file.getvalue()
    text = raw_data.decode("utf-8")
    words = text.split()
    total_chars = len(text)
    
    #Dictionary counting
    freq_dict = {}
    for word in words:
        clean = word.strip(".,!?;:()\"").lower()
        freq_dict[clean] = freq_dict.get(clean, 0) + 1
        
    #Merge Sort
    sorted_freq = merge_sort(list(freq_dict.items()))
    
    # NumPy: Data Processing
    word_lengths = np.array([len(w) for w in words])
    avg_len = np.mean(word_lengths)
    
    #Expected Ratio
    top_10 = sorted_freq[:10]
    saved_bytes = sum((len(word) - 1) * freq for word, freq in top_10)
    projected_size = total_chars - saved_bytes
    expected_ratio = (1 - (projected_size / total_chars)) * 100

    # ZIP Implementation
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr(uploaded_file.name, raw_data)
        
    stats = {
        "top_words": top_10,
        "avg_len": avg_len,
        "expected_ratio": expected_ratio,
        "total_chars": total_chars,
        "projected_size": projected_size
    }
    
    return out.getvalue(), f"shrunk_{uploaded_file.name}.zip", "application/zip", stats