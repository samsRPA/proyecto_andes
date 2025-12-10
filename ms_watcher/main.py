
from pathlib import Path
import sys
from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from app.api.views import getApiRouter
from app.dependencies.Dependencies import Dependencies

from app.infrastucture.config.Settings import load_config
from app.application.dto.HoyPathsDto import HoyPathsDto

# ============ Configuración de logging ============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


  # ============ Configuración de logging ============
def setup_logger(log_path: Path):
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(module)s] %(message)s',
            handlers=[
                logging.FileHandler(log_path, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
               
            ],
        )

logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
    paths = HoyPathsDto.build().model_dump()
    setup_logger(paths["logs_file"])
    config = load_config()
    dependency = Dependencies()
    dependency.settings.override(config)
    app.container = dependency
    db = dependency.data_base()
    producer = dependency.rabbitmq_producer()


    try:
        await producer.connect()
        await db.connect()

        yield

        #keys = await service.getAllkeys()
        #print(keys)
    except Exception as error:
        
        logger.exception("❌ Error durante la ejecución principal", exc_info=error)
    finally:
        try:
            await producer.close()
        except Exception as e:
            logger.warning(f"⚠️ No se pudo cerrar RabbitMQ correctamente: {e}")
        try:
            if db.is_connected:
                await db.close_connection()
        except Exception as error:
            logger.warning(f"⚠️ No se pudo cerrar la DB correctamente: {error}")




app = FastAPI(
    lifespan=lifespan,
    title="Andes API Service",
    description=(
        "notificaciones app"
    ),
    version="0.1.0",
    contact={
        "name": "Rpa Litigando Department",
        "email": "correog@gmail.com",
    },
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/swagger",
    redoc_url="/api/v1/redocs",
)

app.include_router(getApiRouter())

@app.get("/")
def default():
    return {"mensaje": "Hello notificaciones tyba"}

@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
