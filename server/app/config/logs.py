import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class SizedTimedRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        rollover_name = f"{self.baseFilename}.{current_time}"
        
        # Renombrar archivo actual si existe
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, rollover_name)
        
        # Abrir nuevo archivo de log
        self.mode = 'a'
        self.stream = self._open()

        # Gestionar backups antiguos: eliminar si hay más que backupCount
        if self.backupCount > 0:
            log_dir = os.path.dirname(self.baseFilename)
            base_name = os.path.basename(self.baseFilename)
            # Listar archivos que comienzan con el nombre base (incluyendo rotados)
            files = [f for f in os.listdir(log_dir) if f.startswith(base_name + ".")]
            # Ordenar por fecha en nombre, el formato YYYY-MM-DD_HH-MM-SS hace que ordenar alfabéticamente funcione
            files.sort(reverse=True)
            # Borrar los más antiguos si hay más de backupCount
            for old_file in files[self.backupCount:]:
                os.remove(os.path.join(log_dir, old_file))


def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    app_logger = logging.getLogger("my_app_logger")
    app_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = SizedTimedRotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=20 * 1024 * 1024,  # 20 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not app_logger.handlers:
        app_logger.addHandler(file_handler)
        app_logger.addHandler(console_handler)

    return app_logger
      