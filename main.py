import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from backend.routes.dashboard import router as dashboard_router
from backend.routes.assets import router as assets_router
from backend.routes.vulnerabilities import router as vulnerabilities_router
from backend.routes.compliance import router as compliance_router
from backend.routes.phi_risks import router as phi_risks_router
from backend.routes.anomalies import router as anomalies_router
from backend.routes import auth

app = FastAPI(title="HealthSecure API")

# CORS (ALLOW YOUR REACT APP)
allow_origins = os.getenv("FRONTEND_URL", "*").split(",")

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

# Enable Bearer Auth in Swagger (must be called after routers are registered)
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

# Generate OpenAPI schema with auth
app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "HealthSecure Backend is running 🚀"}
