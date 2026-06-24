import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

doc = Document('SUSUN-SKRIPSI-ARIF_BACKUP.docx')
for i, para in enumerate(doc.paragraphs):
    if 'gambar' in para.text.lower() or 'gmabar' in para.text.lower() or 'proses bisnis' in para.text.lower():
        print(f"[{i}] '{para.text[:100]}'")
