# pdf_reader.py
from pypdf import PdfReader
import os
import requests
import tempfile

class PDFReader:
    def __init__(self, pdf_path):
        self.pdf_path = None

        # Verificar se pdf_path é uma URL
        if pdf_path.startswith("http://") or pdf_path.startswith("https://"):
            print(f"🔗 PDF fornecido como URL: {pdf_path}")
            # Baixar o arquivo PDF e armazená-lo temporariamente
            response = requests.get(pdf_path)
            if response.status_code == 200:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                temp_file.write(response.content)
                temp_file.close()
                self.pdf_path = temp_file.name
                print(f"✅ PDF baixado com sucesso e salvo como '{self.pdf_path}'")
            else:
                raise ValueError(f"Erro ao baixar o PDF da URL: {pdf_path}")
        else:
            # Caminho local
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
            self.pdf_path = pdf_path

    def read_pdf(self):
        content = []

        # Abrir e ler o PDF
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

