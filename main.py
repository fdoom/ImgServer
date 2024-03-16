from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI()

def save_uploaded_file(upload_folder: str, file: UploadFile):
    os.makedirs(upload_folder, exist_ok=True)
    with open(os.path.join(upload_folder, file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

@app.post("/upload/")
async def upload_file(upload_folder: str , file: UploadFile = File(...)):
    try:
        save_uploaded_file(upload_folder, file)
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})
    
@app.get("/")
def read_root():
    return {"Hello" : str(os.getcwd())}