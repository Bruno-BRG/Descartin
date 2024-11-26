from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import crud

app = FastAPI(
    title="Weight Data API",
    description="API for managing weight data. Data provided by [Cascais Data](https://data.cascais.pt/)",
    version="1.0.0"
)

class Weight(BaseModel):
    weight: str
    residue_type: str
    date: str

@app.get("/weight/{index}")
def get_weight(index: int):
    result = crud.get_weight(index)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/weight")
def add_weight(weight: Weight):
    result = crud.add_weight(weight.weight, weight.residue_type, weight.date)
    return result

@app.put("/weight/{index}")
def update_weight(index: int, weight: Weight):
    result = crud.update_weight(index, weight.weight, weight.residue_type, weight.date)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.delete("/weight/{index}")
def delete_weight(index: int):
    result = crud.delete_weight(index)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/weight")
def get_all_weights():
    data = crud.load_data()
    return data
