

from ..decorator.decorator import validate_exception
from ..services.heath_check import HealthCheckServices
from ..response import ResponseBuilder, ResponseCodes
from rest_framework.views import APIView

class HealthCheckAPIView(APIView):
    @validate_exception()
    def get(self, request, *args, **kwargs):
        services_helth_check = HealthCheckServices.health_check()
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data = {
                **services_helth_check
            } 
        )