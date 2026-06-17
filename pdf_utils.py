import io
from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text