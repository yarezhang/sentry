from __future__ import absolute_import
from rest_framework import serializers
# from sentry.api.serializers.rest_framework import ListField


class DashboardSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)


class WidgetSerializer(serializers.Serializer):
    # dashboard_order = IntegerField()  # hmmm.... what do we use then?
    display_type = serializers.CharField(required=True)
    # data = ??
