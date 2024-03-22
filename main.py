from fastapi import FastAPI
from m12.routes import auth, contacts
import uvicorn


app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Welcome in users contacts!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)