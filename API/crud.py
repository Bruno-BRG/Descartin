import json

def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

def get_weight(index):
    data = load_data()
    if 0 <= index < len(data):
        return data[index]
    else:
        return {"error": "Index out of range"}

def add_weight(weight, residue_type):
    data = load_data()
    data.append({"weight": weight, "residue_type": residue_type})
    with open('data.json', 'w') as file:
        json.dump(data, file)
    return {"message": "Weight added successfully"}

def update_weight(index, weight):
    data = load_data()
    if 0 <= index < len(data):
        data[index]["weight"] = weight
        with open('data.json', 'w') as file:
            json.dump(data, file)
        return {"message": "Weight updated successfully"}
    else:
        return {"error": "Index out of range"}

def delete_weight(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        with open('data.json', 'w') as file:
            json.dump(data, file)
        return {"message": "Weight deleted successfully"}
    else:
        return {"error": "Index out of range"}
