from rest_framework import serializers

from EaganJones.models import Companies


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies

        fields = ['id', 'companyname', 'cik', 'primarysymbol', 'jsonnn']