from __future__ import absolute_import

from django.db import IntegrityError, transaction
from sentry.api.base import DocSection
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.bases.dashboard import DashboardSerializer
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.models import Dashboard
from rest_framework.response import Response


class OrganizationDashboardsEndpoint(OrganizationEndpoint):
    doc_section = DocSection.ORGANIZATIONS

    def get(self, request, organization):
        """
        Retrieve an Organizations Dashboards
        `````````````````````````````````````
         Retrieve a list of dashboards that are associated with the given organization.
         :pparam string organization_slug: the slug of the organization the
                                          dashboards belongs to.
        :qparam string query: the title of the dashboard being searched for.
        :auth: required
        """
        dashboards = Dashboard.objects.filter(
            organization_id=organization.id
        )
        query = request.GET.get('query')
        if query:
            dashboards = dashboards.objects.filter(
                title__icontains=query,
            )

        return self.paginate(
            request=request,
            queryset=dashboards,
            order_by='title',
            paginator_cls=OffsetPaginator,
            on_results=lambda x: serialize(x, request.user),
        )

    def post(self, request, organization):
        serializer = DashboardSerializer(data=request.DATA, context={'organization': organization})

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        result = serializer.object

        try:
            with transaction.atomic():
                dashboard = Dashboard.objects.create(
                    organization_id=organization.id,
                    title=result['title'],
                    owner=result['owner'],
                    data=result.get('data'),
                )
        except IntegrityError as e:
            # TODO(lb): hmmm this probably shouldn't be e.message?
            return Response(e.message, status=409)

        return Response(serialize(dashboard, request.user), status=201)
