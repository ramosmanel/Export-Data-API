from flask import Blueprint, request, jsonify, send_file
from utils.process import process_data
from utils.excel import generate_excel

export_bp = Blueprint('export', __name__, url_prefix='/api')

class ExportError(Exception):
    pass

@export_bp.route('/export', methods=['POST'])
def export_data():
    try:
        data = request.get_json()
        if data is None:
            raise ExportError("Nenhum JSON foi recebido ou formato inválido")

        processed_data = process_data(data)
        excel_file = generate_excel(processed_data)

        return send_file(excel_file, as_attachment=True, download_name="dados_recebidos.xlsx"), 200

    except ExportError as e:
        raise e
    except Exception as e:
        raise e