from __future__ import absolute_import
from sentry.models import Widget
from sentry.api.serializers import Serializer


class DashboardSerializer(Serializer):
    def serialize(self, obj, attrs, user):
        return {
            'id': obj.id,
            'title': obj.title,
            'owner': obj.owner.id,
            'organization': obj.organization.slug,
            'data': obj.data,
        }


class DashboardWithWidgetsSerializer(DashboardSerializer):
    def get_attrs(self, item_list, user):
        attrs = super(DashboardWithWidgetsSerializer,
                      self).get_attrs(item_list, user)

        dashboard_ids = [item.id for item in item_list]
        widgets = Widget.objects.filter(
            dashboard_id__in=dashboard_ids,
        )
        for item in item_list:
            attrs[item] = {}
            attrs[item]['widgets'] = [
                {
                    'id': w.id,
                    'title': w.title,
                    'display_type': w.display_type,
                    'data': w.data,

                } for w in widgets if w.dashboard_id == item.id
            ]
        return attrs

    def serialize(self, obj, attrs, user):
        data = super(DashboardWithWidgetsSerializer,
                     self).serialize(obj, attrs, user)
        data['widgets'] = attrs['widgets']
        return data
