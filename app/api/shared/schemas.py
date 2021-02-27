from rest_framework import serializers
from rest_framework.schemas import openapi
from rest_framework.schemas.openapi import AutoSchema as DefaultAutoSchema
from rest_framework.schemas.utils import is_list_view


# TODO: follow https://github.com/encode/django-rest-framework/pull/7424/
# As soon as that PR is released in 3.13, the following class can be removed
# and all the references should be renamed to default AutoSchema
class AutoSchema(DefaultAutoSchema):
    def get_components(self, path, method):
        """
        Return components with their properties from the serializer.
        """

        if method.lower() == 'delete':
            return {}

        components = {}

        request_serializer = self.get_request_serializer(path, method)
        response_serializer = self.get_response_serializer(path, method)

        if isinstance(request_serializer, serializers.Serializer):
            component_name = self.get_component_name(request_serializer)
            content = self.map_serializer(request_serializer)
            components.setdefault(component_name, content)

        if isinstance(response_serializer, serializers.Serializer):
            component_name = self.get_component_name(response_serializer)
            content = self.map_serializer(response_serializer)
            components.setdefault(component_name, content)

        return components

    def get_request_body(self, path, method):
        if method not in ('PUT', 'PATCH', 'POST'):
            return {}

        self.request_media_types = self.map_parsers(path, method)

        serializer = self.get_request_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)

        return {
            'content': {
                ct: {'schema': item_schema}
                for ct in self.request_media_types
            }
        }

    def get_responses(self, path, method):
        if method == 'DELETE':
            return {
                '204': {
                    'description': ''
                }
            }

        self.response_media_types = self.map_renderers(path, method)

        serializer = self.get_response_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)

        if is_list_view(path, method, self.view):
            response_schema = {
                'type': 'array',
                'items': item_schema,
            }
            paginator = self.get_paginator()
            if paginator:
                response_schema = paginator.get_paginated_response_schema(response_schema)
        else:
            response_schema = item_schema
        status_code = '201' if method == 'POST' else '200'
        return {
            status_code: {
                'content': {
                    ct: {'schema': response_schema}
                    for ct in self.response_media_types
                },
                # description is a mandatory property,
                # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject
                # TODO: put something meaningful into it
                'description': ""
            }
        }

    def get_request_serializer(self, path, method):
        return self.get_serializer(path, method)

    def get_response_serializer(self, path, method):
        return self.get_serializer(path, method)


# To improve design of API docs generation with High-Level grouping in Redoc
class CustomOpenApiGenerator(openapi.SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(CustomOpenApiGenerator, self).get_schema(request, public)
        schema['x-tagGroups'] = [
            {
                'name': 'Account',
                'tags': ['Me', "Users"]
            },
        ]
        return schema

    def has_view_permissions(self, path, method, view):
        # TODO: follow https://github.com/encode/django-rest-framework/issues/7616 for more information
        return True
