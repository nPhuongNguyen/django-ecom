from apps.catalogue.models.categories import Category
from apps.catalogue.serializers.categories import CategoryListSerializer
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class CategoryListAPI(CreateMixin, ListMixin, DestroyMixin):
    queryset = Category.objects.all()
    serializer_class_list = CategoryListSerializer
    search_fields = ['name']
    ordering_fields = ['name']

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)