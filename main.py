import sys
import os

# Add the 'backend' directory to sys.path to resolve imports when running from the root on Render
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

# Imports
from routes.dashboard import router as dashboard_router
from routes.assets import router as assets_router
from routes.vulnerabilities import router as vulnerabilities_router
from routes.compliance import router as compliance_router
from routes.phi_risks import router as phi_risks_router
from routes.anomalies import router as anomalies_router
from routes import auth

app = FastAPI(title="HealthSecure API")

# Standard CORS Configuration
allow_origins = [
    "https://healthsecure-frontend1.vercel.app",
    "http://localhost:3000",
    "http://localhost:8001"
]

print(f"DEBUG: Active CORS Origins: {allow_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Ensure CORS headers are sent even on 500 errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    origin = request.headers.get("origin", "")
    headers = {}
    if origin in allow_origins:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers=headers,
    )

# Routers
app.include_router(assets_router)
app.include_router(vulnerabilities_router)
app.include_router(dashboard_router)
app.include_router(compliance_router)
app.include_router(phi_risks_router)
app.include_router(anomalies_router)
app.include_router(auth.router)

# Enable Bearer Auth in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="HealthSecure API",
        version="1.0.0",
        description="Security Dashboard API",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "origins": allow_origins
    }

@app.get("/")
def root():
    return {"message": "HealthSecure Backend is running 🚀"}
