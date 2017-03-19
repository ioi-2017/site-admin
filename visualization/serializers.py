from rest_framework import serializers

from visualization.models import Node, Desk, Contestant, Room


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'ip', 'mac_address', 'username', 'property_id', 'connected')


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ('id', 'contestant', 'active_node', 'room', 'x', 'y', 'angle',)


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = ('id', 'name', 'country', 'number',)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name',)
