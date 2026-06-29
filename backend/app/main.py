from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import auth, leads, users, analytics, gorilla

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router,      prefix="/api/v1/auth",      tags=["Auth"])
app.include_router(users.router,     prefix="/api/v1/users",     tags=["Users"])
app.include_router(leads.router,     prefix="/api/v1/leads",     tags=["Leads"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(gorilla.router,   prefix="/api/v1/gorilla",   tags=["Gorilla CRM"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
