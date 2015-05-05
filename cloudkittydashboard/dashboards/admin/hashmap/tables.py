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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon import tabs

from cloudkittydashboard.api import cloudkitty as api


class CreateService(tables.LinkAction):
    name = "createservice"
    verbose_name = _("Create new Service")
    url = 'horizon:admin:hashmap:service_create'
    icon = "create"
    ajax = True
    classes = ("ajax-modal",)


class DeleteService(tables.BatchAction):
    name = "deleteservice"
    verbose_name = _("Delete Service")
    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Service")
    data_type_plural = _("Services")
    icon = "remove"

    def action(self, request, service_id):
        api.cloudkittyclient(request).hashmap.services.delete(
            service_id=service_id
        )


class ServicesTable(tables.DataTable):
    """This table list the available services.

    Clicking on a service name sends you to a ServiceTabs page.
    """
    name = tables.Column('name', verbose_name=_("Name"),
                         link='horizon:admin:hashmap:service')

    class Meta(object):
        name = "services"
        verbose_name = _("Services")
        table_actions = (CreateService,)
        row_actions = (DeleteService,)


class DeleteField(tables.BatchAction):
    name = "deletefield"
    verbose_name = _("Delete Field")
    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Field")
    data_type_plural = _("Fields")
    icon = "remove"

    def action(self, request, field_id):
        api.cloudkittyclient(request).hashmap.fields.delete(
            field_id=field_id
        )


class CreateField(tables.LinkAction):
    name = "createfield"
    verbose_name = _("Create new Field")
    icon = "create"
    ajax = True
    classes = ("ajax-modal",)

    def get_link_url(self, datum=None):
        url = 'horizon:admin:hashmap:field_create'
        service_id = self.table.request.service_id
        return reverse(url, args=[service_id])


class FieldsTable(tables.DataTable):
    """This table lists the available fields for a given service.

    Clicking on a fields sends you to a MappingsTable.
    """
    name = tables.Column('name', verbose_name=_("Name"),
                         link='horizon:admin:hashmap:field')

    class Meta(object):
        name = "fields"
        verbose_name = _("Fields")
        multi_select = False
        row_actions = (DeleteField,)
        table_actions = (CreateField,)


class FieldsTab(tabs.TableTab):
    name = _("Fields")
    slug = "hashmap_fields"
    table_classes = (FieldsTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = True

    def get_fields_data(self):
        client = api.cloudkittyclient(self.request)
        fields = client.hashmap.fields.list(service_id=self.request.service_id)
        return api.identify(fields)


class DeleteMapping(tables.BatchAction):
    name = "deletemapping"
    verbose_name = _("Delete Mapping")
    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Mapping")
    data_type_plural = _("Mappings")
    icon = "remove"

    def action(self, request, mapping_id):
        api.cloudkittyclient(request).hashmap.mappings.delete(
            mapping_id=mapping_id
        )


class CreateServiceMapping(tables.LinkAction):
    name = "createiservicemapping"
    verbose_name = _("Create new Mapping")
    icon = "create"
    ajax = True
    classes = ("ajax-modal",)

    def get_link_url(self, datum=None):
        url = 'horizon:admin:hashmap:service_mapping_create'
        service_id = self.table.request.service_id
        return reverse(url, args=[service_id])


class EditServiceMapping(tables.LinkAction):
    name = "editservicemapping"
    verbose_name = _("Edit Mapping")
    icon = "edit"
    ajax = True
    classes = ("ajax-modal",)

    def get_link_url(self, datum=None):
        url = 'horizon:admin:hashmap:service_mapping_edit'
        return reverse(url, args=[datum.mapping_id])


class ServiceMappingsTable(tables.DataTable):
    cost = tables.Column('cost', verbose_name=_("Cost"))
    type = tables.Column('type', verbose_name=_("Type"))
    group_id = tables.Column('group_id', verbose_name=_("Group"))

    class Meta(object):
        name = "mappings"
        verbose_name = _("Mappings")
        row_actions = (EditServiceMapping, DeleteMapping)
        table_actions = (CreateServiceMapping,)


class CreateFieldMapping(tables.LinkAction):
    name = "createfieldmapping"
    verbose_name = _("Create new Mapping")
    icon = "create"
    ajax = True
    classes = ("ajax-modal",)

    def get_link_url(self, datum=None):
        url = 'horizon:admin:hashmap:field_mapping_create'
        field_id = self.table.request.field_id
        return reverse(url, args=[field_id])


class EditFieldMapping(tables.LinkAction):
    name = "editfieldmapping"
    verbose_name = _("Edit Mapping")
    icon = "edit"
    ajax = True
    classes = ("ajax-modal",)

    def get_link_url(self, datum=None):
        url = 'horizon:admin:hashmap:field_mapping_edit'
        return reverse(url, args=[datum.mapping_id])


class FieldMappingsTable(tables.DataTable):
    value = tables.Column('value', verbose_name=_("Value"))
    cost = tables.Column('cost', verbose_name=_("Cost"))
    type = tables.Column('type', verbose_name=_("Type"))
    group_id = tables.Column('group_id', verbose_name=_("Group"))

    class Meta(object):
        name = "mappings"
        verbose_name = _("Mappings")
        row_actions = (EditFieldMapping, DeleteMapping)
        table_actions = (CreateFieldMapping,)


class MappingsTab(tabs.TableTab):
    name = _("Mappings")
    slug = "hashmap_mappings"
    table_classes = (ServiceMappingsTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = True

    def get_mappings_data(self):
        client = api.cloudkittyclient(self.request)
        mappings = client.hashmap.mappings.list(
            service_id=self.request.service_id
        )
        return api.identify(mappings)


class ServiceTabs(tabs.TabGroup):
    slug = "services_tabs"
    tabs = (FieldsTab, MappingsTab)
    sticky = True
