import io
import os
import zipfile
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

def compress_image(uploaded_file, quality=30):
    #Compresses an image by converting it to JPEG and reducing quality.
    image = Image.open(uploaded_file)
    output_io = io.BytesIO() #Save to memory instead of disk.
    
    # Convert RGBA (transparent) or Paletted images or grayscale to RGB so they can be saved as JPEGs
    if image.mode in ("RGBA", "P", "LA"):
        image = image.convert("RGB")
        
    # Force saving as JPEG for actual lossy compression
    image.save(output_io, format="JPEG", quality=quality, optimize=True)
    
    base_name = os.path.splitext(uploaded_file.name)[0]
    return output_io.getvalue(), f"compressed_{base_name}.jpg", "image/jpeg"

def compress_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.compress_content_streams() #Compreesses only text etc, not images 
        writer.add_page(page)
        
    output_io = io.BytesIO()
    writer.write(output_io)
    
    return output_io.getvalue(), f"compressed_{uploaded_file.name}", "application/pdf"

def compress_text(uploaded_file):
    #Compresses text and CSV files securely into a .zip archive.
    output_io = io.BytesIO()
    
    with zipfile.ZipFile(output_io, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr(uploaded_file.name, uploaded_file.getvalue())
    
    base_name = os.path.splitext(uploaded_file.name)[0]
    return output_io.getvalue(), f"{base_name}_compressed.zip", "application/zip"