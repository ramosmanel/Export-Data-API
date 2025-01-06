from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/export', methods=['POST'])
def export_data():
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Nenhum JSON foi recebido ou formato inválido")

        processed_data = []
        for entry in data:
            processed_entry = {}
            for key, value in entry.items():
                if key == 'id':
                    continue

                if isinstance(value, list) and len(value) == 3 and all(isinstance(i, int) for i in value):
                    try:
                        value = datetime(value[0], value[1], value[2]).strftime('%d/%m/%Y')
                    except ValueError:
                        pass

                elif isinstance(value, list) and len(value) == 2 and all(isinstance(i, int) for i in value):
                    try:
                        value = f"{value[0]:02}:{value[1]:02}"
                    except ValueError:
                        pass

                elif key in ['createdAt', 'updatedAt'] and isinstance(value, (int, float)):
                    try:
                        value = datetime.utcfromtimestamp(value).strftime('%d/%m/%Y %H:%M:%S')
                    except ValueError:
                        pass

                processed_entry[key] = value

            processed_data.append(processed_entry)

            df = pd.DataFrame(processed_data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            ws = writer.sheets['Sheet1']
            for column_cells in ws.columns:
                max_length = max(len(str(cell.value)) for cell in column_cells if cell.value)
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column_cells[0].column_letter].width = adjusted_width

        output.seek(0)

        print("Dados recebidos e planilha gerada com sucesso.")
        return send_file(output, as_attachment=True, download_name="dados_recebidos.xlsx"), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
