from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from ping.models import PingLog
from ping.serializers import PingLogSerializer


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'


class PingLogsAPI(ReadOnlyModelViewSet, mixins.ListModelMixin):
    serializer_class = PingLogSerializer
    filter_fields = ('node', 'connected')
    queryset = PingLog.objects.all()
    pagination_class = Pagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['pagination'] = self.paginator.get_html_context()
        return response
