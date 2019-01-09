from __future__ import absolute_import
from rest_framework import serializers
from sentry.api.serializers.rest_framework.json import JSONField
from sentry.api.fields.user import UserField


class DashboardSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    owner = UserField(required=True)
    data = JSONField(
        required=False,
    )
