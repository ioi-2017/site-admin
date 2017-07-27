from rest_framework import serializers
from visualization.models import Node, Desk, Contestant, Zone, NodeGroup


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'ip', 'mac_address', 'username', 'property_id', 'connected', 'status',)


class NodeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeGroup
        fields = ('id', 'expression', 'name',)


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ('id', 'contestant', 'active_node', 'zone', 'x', 'y', 'angle', 'number', 'identifier',)


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ('id', 'name', 'first_name', 'last_name', 'gender', 'email', 'country', 'team_code', 'number',)


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'name', 'width', 'height',)


class ZoneSerializer(serializers.ModelSerializer):
    floor = FloorSerializer(read_only=True)

    class Meta:
        model = Zone
        fields = ('id', 'name', 'floor', 'width', 'height', 'x', 'y', 'desk_width', 'desk_height',)
