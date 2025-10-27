from apps.auths.models.users import Users
from apps.auths.serializers.users import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin


class UserListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = Users.objects.all()
    serializer_class_list = UserListSerializer
    serializer_class_detail = UserDetailSerializer
    serializer_class_create = UserCreateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs)

class UserDetailAPI(UpdateMixin, DestroyMixin):
    queryset = Users.objects.all()
    serializer_class_update = UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)