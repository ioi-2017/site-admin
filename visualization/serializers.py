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
        fields = ('id', 'contestant', 'active_node', 'zone', 'x', 'y', 'angle',)


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ('id', 'name', 'first_name', 'last_name', 'gender', 'email', 'country', 'number',)


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'name',)
