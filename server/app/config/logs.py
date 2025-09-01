import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Crear carpeta logs si no existe
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Logger principal
    app_logger = logging.getLogger("my_app_logger")
    app_logger.setLevel(logging.INFO)

    # Formato de salida
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Handler para consola (opcional, para ver en terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Evitar duplicar handlers si ya están agregados
    if not app_logger.handlers:
        app_logger.addHandler(file_handler)
        app_logger.addHandler(console_handler)

    return app_logger