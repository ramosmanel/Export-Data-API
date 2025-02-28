import pandas as pd
from io import BytesIO
from utils.process import process_data, DTO_ORDER, COLUMN_MAPPING

def generate_excel(data):
    """Gera o arquivo Excel com os dados processados."""
    processed_data = process_data(data)
    df = pd.DataFrame(processed_data)

    # Garante que todas as colunas existam
    for col in DTO_ORDER:
        if col not in df.columns:
            df[col] = ""

    df = df[DTO_ORDER].rename(columns=COLUMN_MAPPING)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Processos")
        ws = writer.sheets["Processos"]

        for col in ws.columns:
            max_length = max((len(str(cell.value)) for cell in col if cell.value), default=0)
            ws.column_dimensions[col[0].column_letter].width = max_length + 2

    output.seek(0)
    return output
