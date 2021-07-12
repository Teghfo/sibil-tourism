from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Host
from .serializers import HostListSerializer, HostDetailSerializer


class ShowHost(ReadOnlyModelViewSet):
    queryset = Host.objects.all()
    # serializer_class = HostListSerializer

    # lookup_field = 'pk'

    serialzers = {
        'list': HostListSerializer,
        'retrieve': HostDetailSerializer
    }

    def get_serializer_class(self):
        return self.serialzers.get(self.action)

    @action(methods=['get'], detail=True, url_path='get-owner', url_name='get_owner')
    def get_owner(self, request, pk=None):
        host = get_object_or_404(Host, pk=pk)
        return Response({"nickname":host.owner.nickname})