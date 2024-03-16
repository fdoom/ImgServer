from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
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

@app.get("/images/{image_name}")
def get_image(image_name: str, folder_path: str):
    image_path = os.path.join(folder_path, image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.delete("/images/{image_name}")
def delete_image(image_name: str, folder_path: str):
    image_path = os.path.join(folder_path, image_name)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.get("/")
def read_root():
    return {"Hello" : str(os.getcwd())}