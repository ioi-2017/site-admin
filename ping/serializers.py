from rest_framework import serializers

from ping.models import PingLog


class PingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingLog
        fields = ('node', 'event_time', 'connected')
