from django.apps import AppConfig
from django.conf import settings  # import Django settings
import logging

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        logger = logging.getLogger()  # root logger
        logger.info("App is ready, logging works!")

        # Access settings variables
        logger.info("Info: Loaded environment variables:")
        logger.info(f"\tUsing settings for environment: {getattr(settings, 'ENVIRON', 'unknown')}")
        logger.info(f"\tDebug mode: {'ON' if settings.DEBUG else 'OFF'}")
        logger.info(f"\tUsing database: {'PostgreSQL' if getattr(settings, 'USE_POSTGRES') else 'SQLite'}")
