# pdf_reader.py
from pypdf import PdfReader
import os
import requests
import tempfile
from urllib.parse import urlparse

class CustomPDFReader:
    def __init__(self, pdf_path):
        self.pdf_path = None
        self.file_name = None
        if isinstance(pdf_path, str):
            if pdf_path.startswith("http://") or pdf_path.startswith("https://"):
                print(f"🔗 PDF fornecido como URL: {pdf_path}")
                self.file_name = os.path.basename(urlparse(pdf_path).path)
                response = requests.get(pdf_path)
                if response.status_code == 200:
                    temp_dir = tempfile.gettempdir()
                    temp_file_path = os.path.join(temp_dir, self.file_name)
                    with open(temp_file_path, 'wb') as temp_file:
                        temp_file.write(response.content)
                    self.pdf_path = temp_file_path
                    print(f"✅ PDF baixado com sucesso e salvo como '{self.pdf_path}'")
                else:
                    raise ValueError(f"Erro ao baixar o PDF da URL: {pdf_path}")
            else:
                if not os.path.exists(pdf_path):
                    raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
                self.pdf_path = pdf_path
                self.file_name = os.path.basename(self.pdf_path)
            print(f"📂 Nome do arquivo PDF extraído: '{self.file_name}'")
        else:
            raise ValueError("pdf_path must be a string or a file object")

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

