from apps.core.repositories.promotions import PromotionRepository
from apps.core.schema.promotions import PromotionOutputSerializer, PromotionSerializer
from apps.utils.decorator import *


class PromotionService:
    @staticmethod
    @catch_exceptions
    def create_promotion(data):
        promotion = PromotionRepository.create(data)
        promotion_validate_serializer = PromotionSerializer(promotion)
        return promotion_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def get_promotion_by_slug(slug):
        promotion = PromotionRepository.get_by_slug(slug)
        if not promotion:
            return None
        promotion_validate_serializer = PromotionSerializer(promotion)
        return promotion_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def get_all_promotions():
        promotion = PromotionRepository.get_all()
        promotion_validate_serializer = PromotionSerializer(promotion, many = True)
        return promotion_validate_serializer.data
    
    @staticmethod
    @catch_exceptions
    def update_promotion(slug: str, data: dict):
        promotion = PromotionRepository.get_by_slug(slug)
        if not promotion:
            return None
        update_promotion = PromotionRepository.update(promotion, data)
        update_validate_serializer = PromotionOutputSerializer(update_promotion)
        return update_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def delete_promotion(slug):
        promotion = PromotionRepository.get_by_slug(slug)
        if not promotion:
            return None
        delete_promotion = PromotionRepository.delete(promotion)
        promotion_validate_serializer = PromotionOutputSerializer(delete_promotion)
        return promotion_validate_serializer.data
