from django.apps import AppConfig
from django.conf import settings  # import Django settings
import logging

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        logger = logging.getLogger()  # root logger
        api_logger = logging.getLogger('api') # specific logger for 'api'
        data_logger = logging.getLogger('data') # specific logger for 'data'
        celery_logger = logging.getLogger('celery') # specific logger for 'celery'
        db_logger = logging.getLogger('db') # specific logger for 'db'
        nginx_logger = logging.getLogger('nginx') # specific logger for 'nginx'
        # errors_logger = logging.getLogger('errors') # specific logger for 'errors'

        # Access settings variables
        logger.info("Info: Loaded environment variables:")
        logger.info(f"\tUsing settings for environment: {getattr(settings, 'ENVIRON', 'unknown')}")
        logger.info(f"\tDebug mode: {'ON' if settings.DEBUG else 'OFF'}")
        logger.info(f"\tUsing database: {'PostgreSQL' if getattr(settings, 'USE_POSTGRES') else 'SQLite'}")

        api_logger.info("API logger is set up.")
        data_logger.info("Data logger is set up.")
        celery_logger.info("Celery logger is set up.")  
        db_logger.info("DB logger is set up.")  
        nginx_logger.info("Nginx logger is set up.")

        logger.info("App is ready, logging works!")