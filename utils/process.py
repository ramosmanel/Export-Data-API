from datetime import datetime

JSON_TO_DTO_MAPPING = {
    "NUMERO PROCESSO": "processNumber",
    "NUMERO PROCESSO VINCULADO": "linkedProcessNumber",
    "ESTADO": "state",
    "DATA DE RECEBIMENTO BCC": "bccReceivedDate",
    "HORA DE RECEBIMENTO BCC": "bccReceivedTime",
    "DATA DE CAPTURA": "captureDate",
    "HORA DE CAPTURA": "captureTime",
    "DATA DISTRIBUICAO": "distributionDate",
    "SISTEMA DO PROCESSO": "processSystem",
    "AUTOR": "plaintiff",
    "CPF/CNPJ": "cpfCnpj",
    "RÉU": "defendant",
    "ASSUNTO": "subject",
    "TRIBUNAL DE ORIGEM": "originCourt",
    "COMARCA": "district",
    "FORO": "forum",
    "VARA": "court",
    "TIPO DE COMUNICACAO": "communicationType",
    "DATA DE COMUNICACAO": "communicationDate",
    "HORA DE COMUNICACAO": "communicationTime",
    "DATA FINAL DE COMUNICACAO": "communicationEndDate",
    "CLASSE": "class_",
    "VALOR DA CAUSA": "caseValue",
    "DATA DA AUDIENCIA": "hearingDate",
    "HORA AUDIENCIA": "hearingTime",
    "SEGREDO DE JUSTICA": "justiceSecret",
    "NOTA": "note",
    "DESCRICAO OBF": "obfDescription",
    "MULTA": "penalty",
    "VALOR MULTA": "penaltyAmount",
    "TIPO MULTA": "penaltyType",
    "PRAZO FINAL": "deadline",
    "COMPETÊNCIA": "competence",
    "PROCESSO ASSOCIADO": "internalCode",
    "TAGS": "tags",
    "STATUS": "status",
    "ESTADOS": "state",
    "PARA SETOR": "forSector",
    "ATRIBUIDO": "responsible"
}


DTO_ORDER = [
    "processNumber", "linkedProcessNumber", "state", "bccReceivedDate", "bccReceivedTime",
    "captureDate", "captureTime", "distributionDate", "processSystem", "plaintiff",
    "cpfCnpj", "defendant", "subject", "originCourt", "district", "forum", "court",
    "internalCode", "communicationType", "communicationDate", "communicationTime",
    "communicationEndDate", "class_", "caseValue", "hearingDate", "hearingTime",
    "justiceSecret", "note", "obfDescription", "penalty", "penaltyAmount",
    "penaltyType", "deadline", "status", "competence", "forSector", "responsible"
]

COLUMN_MAPPING = {
    "processNumber": "Número do Processo",
    "linkedProcessNumber": "Número do Processo Vinculado",
    "state": "Estado",
    "bccReceivedDate": "Data de Recebimento BCC",
    "bccReceivedTime": "Hora de Recebimento BCC",
    "captureDate": "Data de Captura",
    "captureTime": "Hora de Captura",
    "distributionDate": "Data de Distribuição",
    "processSystem": "Sistema do Processo",
    "plaintiff": "Autor",
    "cpfCnpj": "CPF/CNPJ",
    "defendant": "Réu",
    "subject": "Assunto",
    "originCourt": "Tribunal de Origem",
    "district": "Distrito",
    "forum": "Fórum",
    "court": "Corte",
    "internalCode": "Código Interno",
    "communicationType": "Tipo de Comunicação",
    "communicationDate": "Data da Comunicação",
    "communicationTime": "Hora da Comunicação",
    "communicationEndDate": "Data Final da Comunicação",
    "class_": "Classe",
    "caseValue": "Valor da Causa",
    "hearingDate": "Data da Audiência",
    "hearingTime": "Hora da Audiência",
    "justiceSecret": "Segredo de Justiça",
    "note": "Nota",
    "forSector": "Para Setor",
    "obfDescription": "Descrição OBF",
    "penalty": "Multa",
    "penaltyAmount": "Valor da Multa",
    "penaltyType": "Tipo de Multa",
    "deadline": "Prazo Final",
    "responsible": "Atribuido",
    "status": "Status",
    "competence": "Competência"
}


def convert_json_keys(data):
    """Converte as chaves do JSON para os nomes esperados no código."""
    converted_data = []
    for entry in data:
        converted_entry = {JSON_TO_DTO_MAPPING.get(k, k): v for k, v in entry.items()}
        converted_data.append(converted_entry)
    return converted_data


def process_value(key, value):
    try:
        if isinstance(value, bool):
            return "Sim" if value else "Não"

        if isinstance(value, list):
            if len(value) == 3 and all(isinstance(i, int) for i in value):
                # Verifica se é uma DATA no formato [YYYY, MM, DD]
                if key.lower().endswith("date") or key.lower().startswith("data") or key.lower() == "deadline":
                    return f"{value[2]:02}/{value[1]:02}/{value[0]:04}"  # DD/MM/YYYY

                # Caso contrário, assume que é uma HORA (HH, MM, SS)
                return f"{value[0]:02}:{value[1]:02}:{value[2]:02}"  # HH:mm:ss

            elif len(value) == 4 and all(isinstance(i, int) for i in value):
                # Formata como HH:mm:ss (ignorando nanossegundos)
                return f"{value[0]:02}:{value[1]:02}:{value[2]:02}"

            elif len(value) == 2 and all(isinstance(i, int) for i in value):
                # Formata como HH:mm
                return f"{value[0]:02}:{value[1]:02}"

            elif key.lower() == 'tags' or key.lower() == 'state' or key.lower() == 'forsector':
                return ", ".join(map(str, value))

        elif key in ['createdAt', 'updatedAt'] and isinstance(value, (int, float)):
            return datetime.utcfromtimestamp(value).strftime('%d/%m/%Y %H:%M:%S')

        if key.lower() in ['penaltyamount', 'casevalue'] and isinstance(value,(int, float)):
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        return value
    except Exception as e:
        return str(e)


def process_data(data):
    """Processa os valores do JSON e aplica formatação."""
    converted_data = convert_json_keys(data)
    processed_data = []

    for entry in converted_data:
        processed_entry = {k: process_value(k, entry.get(k, None)) for k in DTO_ORDER}
        processed_data.append(processed_entry)

    return processed_data
