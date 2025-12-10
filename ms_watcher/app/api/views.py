from fastapi import APIRouter

from app.api.routes import proceeding_andes_routes

apiRouter = APIRouter(prefix="/api/v1")
apiRouter.include_router(proceeding_andes_routes.router, tags=["keys"])

def getApiRouter():
    return apiRouter