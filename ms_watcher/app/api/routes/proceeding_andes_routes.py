from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from app.dependencies.Dependencies import Dependencies
from app.application.dto.ProceedingsDto import ProceedingsDto
from app.domain.interfaces.IPublishService import IPublishService




router = APIRouter()

@router.post(
    "/proceedings/queues_andes",
    response_model=ProceedingsDto,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED
)
@inject
async def publishAllProceedings(
        publish_service: IPublishService = Depends(Provide[Dependencies.publish_service])
):
    try:
        raw_proceedings = await publish_service.publishProceedings()
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content="✔️ Mensajes enviados a las cola de andes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


