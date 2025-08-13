from rest_framework.views import APIView
from apps.core.schema import ProductSerializer
from apps.core.services.products import ProductService
from apps.utils.decorator import validate_serializer
from rest_framework.response import Response
# Create your views here.

class ProductView(APIView):
    @validate_serializer(ProductSerializer)
    def post(self, request):
        serializer = request.validated_data
        product = ProductService.create_product(serializer)

        return Response(
            {
                "statusCode": 1,
                "message": "Thành công",
                "data": ProductSerializer(product).data
            }
        )