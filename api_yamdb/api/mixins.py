from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from api.permissions import AdminOrReadOnly


class ListCreateDestroyViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
