import uvicorn

from src.configs.server import server_settings
from src.infrastructure.fastapi.app import create_app
from src.infrastructure.logger.logger import LoggerConfig

app = create_app()


def main() -> None:
    LoggerConfig.setup_logger()

    uvicorn.run(app, host=server_settings.HOST, port=server_settings.PORT, log_config=None)
