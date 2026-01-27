from fastapi import FastAPI

app = FastAPI(title="AI CI/CD Backend")

@app.get("/health")
def health():
    return {"status": "ok"}
