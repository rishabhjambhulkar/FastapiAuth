from fastapi import FastAPI
from fastapi.responses import JSONResponse
from user.routes import router as  user_router




app = FastAPI()

app.include_router(user_router)


@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})

@app.get('/check')
def health_check_check():
    return JSONResponse(content={"status": "check"})
