# pdf_reader.py

import os
from pypdf import PdfReader

class PDFReader:
    def __init__(self, pdf_path):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
        self.pdf_path = pdf_path

    def read_pdf(self):
        content = []

        with open(self.pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    content.append(text)
                else:
                    print(f"⚠️ Aviso: Não foi possível extrair texto da página {page_num + 1}")
        print(f"✅ PDF '{self.pdf_path}' lido com sucesso. Total de páginas: {len(content)}")
        return content
