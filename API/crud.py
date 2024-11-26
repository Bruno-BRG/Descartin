import json
from datetime import datetime

JSON_FILEPATH = 'data.json'

def load_data():
    with open(JSON_FILEPATH, 'r') as file:
        data = json.load(file)
    return data

def get_weight(index):
    data = load_data()
    if 0 <= index < len(data):
        return data[index]
    else:
        return {"error": "Index out of range"}

def add_weight(weight, residue_type, date):
    data = load_data()
    new_entry = {"weight": weight, "residue_type": residue_type, "date": parse_date(date)}
    data.append(new_entry)
    with open(JSON_FILEPATH, 'w') as file:
        json.dump(data, file)
    return {"message": "Weight added successfully"}

def update_weight(index, weight):
    data = load_data()
    if 0 <= index < len(data):
        data[index]['weight'] = weight
        with open(JSON_FILEPATH, 'w') as file:
            json.dump(data, file)
        return {"message": "Weight updated successfully"}
    else:
        return {"error": "Index out of range"}

def delete_weight(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        with open(JSON_FILEPATH, 'w') as file:
            json.dump(data, file)
        return {"message": "Weight deleted successfully"}
    else:
        return {"error": "Index out of range"}

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
