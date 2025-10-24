from apps.auths.models.users import Users
from apps.auths.serializers.users import UserListSerializer, UserDetailSerializer, UserCreateSerializer
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin


class UserListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = Users.objects.all()
    serializer_class_list = UserListSerializer
    serializer_class_detail = UserDetailSerializer
    serializer_class_create = UserCreateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)