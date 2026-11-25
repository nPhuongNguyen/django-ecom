from django.apps import AppConfig
import sys

class QdrantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.qdrant'
    
    # def ready(self):
    #     # Kiểm tra để tránh chạy 2 lần khi dev với runserver auto-reload
    #     if 'runserver' in sys.argv:
    #         # Import tại đây để tránh lỗi AppRegistryNotReady
    #         from apps.qdrant.services.qdrant_service import QdrantService
            
    #         try:
    #             QdrantService.init_collection(collection_name="django-ecom-qdrant", vector_size=384)
    #             print("--- [Qdrant] Successfully initialized collection: django-ecom-qdrant ---")
    #         except Exception as e:
    #             print(f"--- [Qdrant] Could not connect to Qdrant on start: {e} ---")