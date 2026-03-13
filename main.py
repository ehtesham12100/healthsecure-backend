import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Absolute imports from the backend package
from backend.routes.dashboard import router as dashboard_router
from backend.routes.assets import router as assets_router
from backend.routes.vulnerabilities import router as vulnerabilities_router
from backend.routes.compliance import router as compliance_router
from backend.routes.phi_risks import router as phi_risks_router
from backend.routes.anomalies import router as anomalies_router
from backend.routes import auth

app = FastAPI(title="HealthSecure API")

# Standard CORS Configuration
allow_origins = [
    "https://healthsecure-frontend1.vercel.app",
    "http://localhost:3000",
    "http://localhost:8001"
]

# Add FRONTEND_URL if provided (stripping whitespace and removing *)
env_origins = os.getenv("FRONTEND_URL", "")
if env_origins:
    extra = [o.strip() for o in env_origins.split(",") if o.strip() and o.strip() != "*"]
    allow_origins.extend(extra)

# Remove duplicates
allow_origins = list(set(allow_origins))

print(f"DEBUG: Active CORS Origins: {allow_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "origins": allow_origins,
        "env_frontend": os.getenv("FRONTEND_URL")
    }

@app.get("/")
def root():
    return {"message": "HealthSecure Backend is running 🚀"}
