from fastapi import FastAPI

app = FastAPI(title="FATHER DZ18 Agent Service", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "father-dz18-agent"}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "father-dz18-agent",
        "purpose": "OTUS Lesson 18 IaC/CI/CD delivery lab",
        "status": "engineering-draft",
    }
