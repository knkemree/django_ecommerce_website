import json
import urllib
from urllib import request

import jsonfield
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Companies(models.Model):
    companyname = models.CharField(max_length=200, db_index=True)
    table = models.TextField(blank=True, null=True)
    cik = models.IntegerField(blank=True, null=True)
    primarysymbol = models.CharField(max_length=200, db_index=True)
    markettier = models.CharField(max_length=200, blank=True, null=True)
    sicdescription = models.CharField(max_length=1000, blank=True, null=True)
    jsonnn = jsonfield.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.companyname

    class Meta:
        ordering = ('companyname','cik','primarysymbol')

    index_together = (('id', 'primarysymbol'),)


    def get_absolute_url(self):
        return reverse('EaganJones:company_detail',
                       args=[self.id, self.primarysymbol])











