# Copyright 2015 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging


from django.utils.translation import ugettext_lazy as _
from horizon import forms

from cloudkittydashboard.api import cloudkitty as api

LOG = logging.getLogger(__name__)


class CreateServiceForm(forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"))

    def handle(self, request, data):
        name = data['name']
        LOG.info('Creating service with name %s' % (name))
        return api.cloudkittyclient(request).hashmap.services.create(name=name)


class CreateFieldForm(forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"))
    service_id = forms.CharField(label=_("Service ID"),
                                 widget=forms.TextInput(
                                 attrs={'readonly': 'readonly'}))

    def handle(self, request, data):
        name = data['name']
        service_id = data['service_id']
        LOG.info('Creating field with name %s' % (name))
        field_client = api.cloudkittyclient(request).hashmap.fields
        return field_client.create(name=name, service_id=service_id)


class CreateMappingForm(forms.SelfHandlingForm):
    cost = forms.DecimalField(label=_("Cost"))
    type = forms.ChoiceField(label=_("Type"),
                             choices=(("flat", _("Flat")),
                                      ("rate", _("Rate")),
                                      ("threshold", _("Threshold"))))
    group_id = forms.CharField(label=_("Group"), required=False)

    def handle(self, request, data):
        mapping_client = api.cloudkittyclient(request).hashmap.mappings
        mapping = {k: v for k, v in data.items() if v and v != ''}
        return mapping_client.create(**mapping)


class CreateFieldMappingForm(CreateMappingForm):
    field_id = forms.CharField(label=_("Field ID"),
                               widget=forms.TextInput(
                               attrs={'readonly': 'readonly'}),
                               required=False)
    value = forms.CharField(label=_("Value"))

    def __init__(self, *args, **kwargs):
        super(CreateFieldMappingForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['value',
                                'cost',
                                'type',
                                'group_id',
                                'field_id']


class CreateServiceMappingForm(CreateMappingForm):
    service_id = forms.CharField(label=_("Service ID"),
                                 widget=forms.TextInput(
                                 attrs={'readonly': 'readonly'}),
                                 required=False)


class EditServiceMappingForm(CreateServiceMappingForm):
    mapping_id = forms.CharField(label=_("Mapping ID"),
                                 widget=forms.TextInput(
                                 attrs={'readonly': 'readonly'}))

    def handle(self, request, data):
        mapping_client = api.cloudkittyclient(request).hashmap.mappings
        mapping = {k: v for k, v in data.items() if v and v != ''}
        mapping['mapping_id'] = self.initial['mapping_id']
        return mapping_client.update(**mapping)


class EditFieldMappingForm(CreateFieldMappingForm):
    mapping_id = forms.CharField(label=_("Mapping ID"),
                                 widget=forms.TextInput(
                                 attrs={'readonly': 'readonly'}))

    def handle(self, request, data):
        mapping_client = api.cloudkittyclient(request).hashmap.mappings
        mapping = {k: v for k, v in data.items() if v and v != ''}
        mapping['mapping_id'] = self.initial['mapping_id']
        return mapping_client.update(**mapping)
