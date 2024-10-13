from admin.llm.index_manager.local_index_manager import LocalIndexGenerator
from admin.llm.pdf_reader.pdf_reader import CustomPDFReader

class adminServices:

    def __init__(self):
        pass
    
    def local_create_index_services(self, data):
        pdf_link = data.get("pdf_link")
        client_id = data.get("client_id")
        reader = CustomPDFReader(pdf_link)
        index_generator = LocalIndexGenerator()
        if not pdf_link:
            return {"status": "error", "message": "Link do PDF não fornecido."}, 400
        try:
            index_generator.client_id = client_id
            index_name = reader.file_name
            pdf_content = reader.read_pdf()
            index = index_generator.create_index(pdf_content, index_name=index_name, client_id=client_id)
            index_generator.db_manager.save_index_metadata(
            client_id=client_id,
            index_name=index_name,
            file_name=f"{index_name}.pkl"
            )
            return {"status": "success", "message": "Índice criado com sucesso."}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500