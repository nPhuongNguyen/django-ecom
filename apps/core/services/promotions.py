from apps.core.repositories.promotions import PromotionRepository


class PromotionService:
    @staticmethod
    def create_promotion(data):
        return PromotionRepository.create(data)

    @staticmethod
    def get_product_by_slug(slug):
        return PromotionRepository.get_by_slug(slug)

    @staticmethod
    def get_all_promotions():
        return PromotionRepository.get_all()
    
    @staticmethod
    def update_product(slug, data):
        product = PromotionRepository.get_by_slug(slug)
        if not product:
            return None
        return PromotionRepository.update(product, data)

    @staticmethod
    def delete_product(slug):
        product = PromotionRepository.get_by_slug(slug)
        if not product:
            return None
        return PromotionRepository.delete(product)
