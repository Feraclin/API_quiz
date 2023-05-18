from api.app.app import app as FastAPIApp

app = FastAPIApp

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(FastAPIApp, host="0.0.0.0", port=8000)
