from rest_framework import serializers

from visualization.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('ip', 'mac_address', 'username', 'property_id', 'connected')
