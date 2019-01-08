from __future__ import absolute_import

import six
from sentry.api.serializers import Serializer, register
from sentry.models import Dashboard


@register(Dashboard)
class DashboardSerializer(Serializer):

    def serialize(self, obj, attrs, user, *args, **kwargs):
        data = {
            'id': six.text_type(obj.id),
            'title': obj.title,
            'organization': six.text_type(obj.organization.id),
            'data': obj.data,
            'dateAdded': obj.date_added,
            'owner': obj.owner.id,
        }

        return data
