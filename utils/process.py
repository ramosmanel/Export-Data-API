from datetime import datetime


def process_value(key, value):
    try:
        if key == 'id':
            return None

        if isinstance(value, list):
            if len(value) == 3 and all(isinstance(i, int) for i in value):
                # Formatar como HH:mm:ss
                return f"{value[0]:02}:{value[1]:02}:{value[2]:02}"

            elif len(value) == 4 and all(isinstance(i, int) for i in value):
                # Ignorar nanossegundos e formatar como HH:mm:ss
                return f"{value[0]:02}:{value[1]:02}:{value[2]:02}"

            elif len(value) == 2 and all(isinstance(i, int) for i in value):
                # Formatar como HH:mm
                return f"{value[0]:02}:{value[1]:02}"

            elif key == 'TAGS':
                return ", ".join(map(str, value))

        elif key in ['createdAt', 'updatedAt'] and isinstance(value, (int, float)):
            return datetime.utcfromtimestamp(value).strftime('%d/%m/%Y %H:%M:%S')

        return value
    except ValueError:
        return value


def process_data(data):
    if not isinstance(data, list):
        raise ValueError("Os dados recebidos devem ser uma lista de objetos JSON.")

    processed_data = [
        {k: process_value(k, v) for k, v in entry.items() if process_value(k, v) is not None}
        for entry in data
    ]

    return processed_data
