import pandas as pd
from io import BytesIO

def generate_excel(data):
    df = pd.DataFrame(data)
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        ws = writer.sheets['Sheet1']

        for column_cells in ws.columns:
            max_length = max((len(str(cell.value)) for cell in column_cells if cell.value), default=0)
            ws.column_dimensions[column_cells[0].column_letter].width = max_length + 2

    output.seek(0)
    return output