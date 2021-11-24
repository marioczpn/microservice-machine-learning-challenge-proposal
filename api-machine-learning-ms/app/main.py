from fastapi import FastAPI

from api.router import face_detection_api

app = FastAPI()
app.include_router(face_detection_api.router)


@app.get("/health")
def main():
    return {"message": "Api is up and running"}
