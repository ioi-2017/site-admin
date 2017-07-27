import svgwrite
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import Context, Template
from django.urls import reverse
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from visualization.models import Zone, Node, Desk, Contestant, NodeGroup
from visualization.serializers import NodeSerializer, DeskSerializer, ContestantSerializer, ZoneSerializer, \
    NodeGroupSerializer


class ExportView(View):
    def get(self, request):
        template = Template(request.GET.get('template', ''))
        context = Context({"Nodes": Node.objects.all(),
                           "Desks": Desk.objects.all(),
                           "Contestants": Contestant.objects.all(),
                           "Zones": Zone.objects.all()})
        return HttpResponse(template.render(context))


class NodeGroupsViewAPI(ModelViewSet):
    serializer_class = NodeGroupSerializer
    queryset = NodeGroup.objects.all()

    def list(self, request, **kwargs):
        results = []
        nodes = list(Node.objects.prefetch_related('desk', 'desk__zone'))

        for group in NodeGroup.objects.order_by('id').all():
            group_nodes = []
            expression_as_func = eval("lambda node: " + group.expression)
            for node in nodes:
                if expression_as_func(node):
                    group_nodes.append(node)
            results.append({'id': group.id, 'name': group.name, 'expression': group.expression,
                            'nodes': [NodeSerializer(node).data for node in group_nodes]})
        return JsonResponse(results, safe=False)


class NodeGroupsRenderView(View):
    def get(self, request):
        group = NodeGroup(expression=request.GET['expression'])
        results = [NodeSerializer(node).data for node in group.nodes()]
        return JsonResponse(results, safe=False)


class RetrieveIPView(View):
    def get(self, request, ip):
        node = Node.objects.get(ip=ip)
        desk = node.desk
        contestant = desk.contestant
        return JsonResponse({
            'node': {
                'ip': node.ip,
                'mac': node.mac_address,
            },
            'contestant': {
                'name': contestant.name,
                'country': contestant.team_code,
                'number': contestant.number,
                'id': contestant.dashed_identifier,
            },
            'desk': {
                'zone': desk.zone.name,
                'number': desk.number,
                'map': reverse('visualization:node-map', kwargs={'ip': ip}),
                'id': desk.identifier,
            },
        }, safe=False)


class RetrieveDeskMap(View):
    def get(self, request, ip):
        desk = Node.objects.get(ip=ip).desk
        desk_width, desk_height = desk.zone.desk_width, desk.zone.desk_height
        image = svgwrite.Drawing(size=("%dpx" % desk.zone.width, "%dpx" % desk.zone.height))

        for other_desk in desk.zone.desk_set.all():
            x, y, angle = other_desk.x * desk.zone.width, other_desk.y * desk.zone.height, other_desk.angle
            image.add(image.rect((x - desk_width / 2, y - desk_height / 2), (desk_width, desk_height),
                                 fill='#666666' if other_desk.id == desk.id else 'white', stroke='#666666',
                                 transform='rotate(%d %f %f)' % (angle, x, y)))

        return HttpResponse(image.tostring(), content_type="image/svg+xml")


class NodesAPI(ModelViewSet):
    serializer_class = NodeSerializer
    filter_fields = ('id', 'ip', 'mac_address', 'username', 'property_id', 'connected')
    queryset = Node.objects.all()


class DesksAPI(ModelViewSet):
    serializer_class = DeskSerializer
    filter_fields = ('contestant', 'active_node', 'zone',)
    queryset = Desk.objects.all()


class ContestantsAPI(ModelViewSet):
    serializer_class = ContestantSerializer
    filter_fields = ('country', 'number',)
    queryset = Contestant.objects.all()


class ZonesAPI(ModelViewSet):
    serializer_class = ZoneSerializer
    filter_fields = ('name',)
    queryset = Zone.objects.order_by('id')

    @staticmethod
    def get_zone_data(zone):
        data = ZoneSerializer(zone).data
        data['desks'] = []
        for desk in Desk.objects.filter(zone=zone).prefetch_related('contestant', 'active_node'):
            deskData = DeskSerializer(desk).data
            deskData['active_node'] = NodeSerializer(desk.active_node).data
            deskData['contestant'] = ContestantSerializer(desk.contestant).data
            data['desks'].append(deskData)
        return data

    def retrieve(self, request, *args, pk=None, **kwargs):
        zone = get_object_or_404(self.queryset, pk=pk)
        return Response(self.get_zone_data(zone))

    def list(self, request, **kwargs):
        data = []
        for zone in self.filter_queryset(self.get_queryset()):
            data.append(self.get_zone_data(zone))
        return Response(data)
