from __future__ import absolute_import
from rest_framework import serializers
from sentry.api.serializers.rest_framework import ListField
from sentry.models import WidgetDisplayTypes


class DashboardSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    data = ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
    )


class WidgetSerializer(serializers.Serializer):
    dashboard_order = serializers.IntegerField(min_value=0, required=True)
    display_type = serializers.CharField(required=True)
    data = ListField(
        child=serializers.CharField(),
        required=True,
    )

    def validate_display_type(self, attrs, source):
        display_type = attrs[source]
        if display_type not in WidgetDisplayTypes.__members__:
            raise ValueError('Widget display_type %s not recognized.' % display_type)

        return attrs
