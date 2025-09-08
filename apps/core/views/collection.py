from rest_framework.views import APIView
from apps.core.schema.collection import *
from apps.core.services.collection import CollectionService
from apps.utils.decorator import *
from apps.utils.response import ResponseUtil as res
# Create your views here.

class CollectionView(APIView):
    @catch_exceptions
    @validate_serializer(CollectionInputSerializer)
    def post(self, request):
        serializer = request.validated_data
        collection = CollectionService.create_collection(serializer)
        return res.response_success(data=collection)

    @catch_exceptions
    def get(self, request, sku=None):
        if sku:
            collection = CollectionService.get_collection_by_sku(sku)
            if not collection:
                return res.response_error(message="Collection không tồn tại!")
            return res.response_success(data=collection)

        # Nếu không có slug → trả về list
        collections = CollectionService.get_all_collections()
        return res.response_success(data=collections)

    @catch_exceptions
    @validate_serializer(CollectionSerializer)
    def put(self, request, sku, *args, **kwargs):
        validated_data = request.validated_data
        collection = CollectionService.update_collection(sku, validated_data)
        if not collection:
            return res.response_error(message="Collection không tồn tại!")
        return res.response_success(message="Cập nhật bộ sưu tập thành công", data=collection)

    @catch_exceptions
    def delete(self, request, sku, *args, **kwargs):
        collection = CollectionService.delete_collection(sku)
        if not collection:
            return res.response_error(message="Collection không tồn tại!")
        return res.response_success(message="Xóa bộ sưu tập thành công", data=collection)
