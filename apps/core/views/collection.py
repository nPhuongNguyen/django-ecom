from rest_framework.views import APIView
from apps.core.schema.collection import CollectionSerializer
from apps.core.services.collection import CollectionService
from apps.utils.decorator import validate_serializer
from rest_framework.response import Response
# Create your views here.

class CollectionView(APIView):
    @validate_serializer(CollectionSerializer)
    def post(self, request):
        serializer = request.validated_data
        collection = CollectionService.create_collection(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": CollectionSerializer(collection).data
            }
        )
    def get(self, request, slug=None):
        if slug:
            collection = CollectionService.get_collection_by_slug(slug)
            if not collection:
                return Response({
                    "statusCode": 0,
                    "message": "Collection not found",
                    "data": None
                })
            return Response({
                "statusCode": 1,
                "message": "Thành công",
                "data": CollectionSerializer(collection).data
            })
        # Nếu không có slug → trả về list
        collections = CollectionService.get_all_collections()
        return Response({
            "statusCode": 1,
            "message": "Thành công",
            "data": CollectionSerializer(collections, many=True).data
        })


    @validate_serializer(CollectionSerializer)
    def put(self, request, slug, *args, **kwargs):
        validated_data = request.validated_data
        collection = CollectionService.update_collection(slug, validated_data)
        if not collection:
            return Response({
                "statusCode": 0,
                "message": "Collection not found",
                "data": None
            })
        return Response({
            "statusCode": 1,
            "message": "Cập nhật bộ sưu tập thành công",
            "data": CollectionSerializer(collection).data
        })
    
    def delete(self, request, slug, *args, **kwargs):
        collection = CollectionService.delete_collection(slug)
        if not collection:
            return Response({
                "statusCode": 0,
                "message": "Collection not found",
                "data": None
            })
        
        return Response({
            "statusCode": 1,
            "message": "Xóa bộ sưu tập thành công",
            "data": CollectionSerializer(collection).data
        })
    
