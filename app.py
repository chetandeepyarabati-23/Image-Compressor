import io
import os
from PIL import Image
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure Streamlit Page
st.set_page_config(
    page_title="JEE Main Document Prep Suite",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Premium Dark UI CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    h1, h2, h3, p, label {
        color: #f3f4f6 !important;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="column"] {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="column"]:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.6);
        transform: scale(1.02);
    }
    div[data-testid="stFileUploader"] {
        background-color: #1e293b;
        border: 1px dashed #475569;
        border-radius: 12px;
        padding: 10px;
    }
    .badge {
        background-color: #1e1b4b;
        color: #818cf8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #3730a3;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# App Header
st.title("JEE Main Form-Prep Suite")
st.markdown(
    "Upload raw scans or phone photos below for automated, NTA-compliant"
    " compression."
)
st.write("---")

# Three Side-by-Side Options
col1, col2, col3 = st.columns(3, gap="large")

# --- COLUMN 1: PASSPORT PHOTO ---
with col1:
  st.subheader("Passport Photo")
  st.markdown(
      '<span class="badge">10 KB - 200 KB | JPG</span>', unsafe_allow_html=True
  )
  st.write("")

  photo_file = st.file_uploader(
      "Upload Passport Photo", type=["jpg", "jpeg", "png"], key="photo"
  )

  if photo_file:
    photo_img = Image.open(photo_file).convert("RGB")
    st.image(photo_img, use_container_width=True)

    if st.button("Compress Photo", key="btn_photo"):
      buffer = io.BytesIO()
      quality = 95
      while quality > 5:
        buffer.seek(0)
        buffer.truncate(0)
        photo_img.save(buffer, format="JPEG", quality=quality)
        size_kb = buffer.tell() / 1024
        if size_kb <= 180:
          break
        quality -= 5

      st.success(f"Final Size: **{size_kb:.1f} KB**")
      st.download_button(
          label="Download Photo",
          data=buffer.getvalue(),
          file_name="Passport_Photo.jpg",
          mime="image/jpeg",
          use_container_width=True,
      )

# --- COLUMN 2: SIGNATURE ---
with col2:
  st.subheader("Signature")
  st.markdown(
      '<span class="badge">10 KB - 100 KB | JPG</span>', unsafe_allow_html=True
  )
  st.write("")

  sig_file = st.file_uploader(
      "Upload Signature", type=["jpg", "jpeg", "png"], key="sig"
  )

  if sig_file:
    sig_img = Image.open(sig_file).convert("RGB")
    st.image(sig_img, use_container_width=True)

    if st.button("Compress Signature", key="btn_sig"):
      buffer = io.BytesIO()
      quality = 90
      while quality > 5:
        buffer.seek(0)
        buffer.truncate(0)
        sig_img.save(buffer, format="JPEG", quality=quality)
        size_kb = buffer.tell() / 1024
        if size_kb <= 90:
          break
        quality -= 5

      st.success(f"Final Size: **{size_kb:.1f} KB**")
      st.download_button(
          label="Download Signature",
          data=buffer.getvalue(),
          file_name="Signature.jpg",
          mime="image/jpeg",
          use_container_width=True,
      )

# --- COLUMN 3: 10TH MARKSHEET PDF ---
with col3:
  st.subheader("10th Marksheet")
  st.markdown(
      '<span class="badge">50 KB - 300 KB | PDF</span>', unsafe_allow_html=True
  )
  st.write("")

  doc_file = st.file_uploader(
      "Upload Marksheet Scan", type=["jpg", "jpeg", "png"], key="doc"
  )

  if doc_file:
    doc_img = Image.open(doc_file).convert("RGB")
    st.image(doc_img, use_container_width=True)

    if st.button("Generate & Compress PDF", key="btn_pdf"):
      pdf_buffer = io.BytesIO()
      c = canvas.Canvas(pdf_buffer, pagesize=letter)
      width, height = letter

      temp_img_path = "temp_marksheet.jpg"
      doc_img.save(temp_img_path, "JPEG", quality=75)
      c.drawImage(temp_img_path, 30, 80, width=550, height=700)
      c.save()

      pdf_data = pdf_buffer.getvalue()
      pdf_size_kb = len(pdf_data) / 1024

      if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

      st.success(f"Final PDF Size: **{pdf_size_kb:.1f} KB**")
      st.download_button(
          label="Download Marksheet PDF",
          data=pdf_data,
          file_name="Class10_Marksheet.pdf",
          mime="application/pdf",
          use_container_width=True,
      )