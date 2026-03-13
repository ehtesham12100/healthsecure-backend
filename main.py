import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from routes.dashboard import router as dashboard_router
from routes.assets import router as assets_router
from routes.vulnerabilities import router as vulnerabilities_router
from routes.compliance import router as compliance_router
from routes.phi_risks import router as phi_risks_router
from routes.anomalies import router as anomalies_router
from routes import auth

app = FastAPI(title="HealthSecure API")

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# CORS (ALLOW EVERYTHING FOR DEPLOYMENT)
# Note: This is the 'Nuclear Option' to fix persistent deployment blocks
@app.middleware("http")
async def dynamic_cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response()
    else:
        response = await call_next(request)
    
    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    
    return response

# Standard middleware as backup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be false if origins is *
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    origin = request.headers.get("origin")
    print(f"DEBUG: Request Origin: {origin}")
    response = await call_next(request)
    return response

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

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "allowed_origins": allow_origins,
        "env_frontend_url": os.getenv("FRONTEND_URL")
    }

@app.get("/")
def root():
    return {"message": "HealthSecure Backend is running 🚀"}
