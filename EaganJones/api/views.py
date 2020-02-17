from rest_framework import generics

from EaganJones.api.serializers import CompaniesSerializer
from EaganJones.models import Companies


class CompaniesListView(generics.ListAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
class CompaniesDetailView(generics.RetrieveAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer