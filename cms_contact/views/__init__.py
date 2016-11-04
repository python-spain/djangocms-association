import json

import six
from cities.models import City, PostalCode, Subregion, Region
from django.contrib.gis.db.models.functions import GeomValue
from django.contrib.gis.geos import Point
from django.db.models.expressions import CombinedExpression, F
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View


class AjaxView(View):
    safe = True

    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT']:
            kwargs.setdefault('data', request.POST or
                              json.loads(request.body if six.PY2 else request.body.decode('utf-8')))
        response = super(AjaxView, self).dispatch(request, *args, **kwargs) or {}
        if isinstance(response, HttpResponse):
            return response
        return JsonResponse(response, safe=self.safe)


class AjaxPopulateAddress(AjaxView):
    safe = False

    def get(self, request):
        return {"foo": 3}

    def post(self, request, data):
        if not data.get('name') and not data.get('lat'):
            return HttpResponseServerError("Name or coords is required.")
        if data.get('name'):
            model = {'city': City, 'subregion': Subregion, 'region': Region}.get(data.get('model'))
            if not model:
                return HttpResponseServerError("Invalid model: {}".format(data.get('model')))
            obj = get_object_or_404(model, pk=data['name'])
        else:
            # http://stackoverflow.com/a/35079313
            pnt = Point(float(data.get('lon', 0)), float(data.get('lat', 0)), srid=4326)
            order_by_expression = CombinedExpression(F('location'), '<->', GeomValue(pnt))
            try:
                obj = City.objects.order_by(order_by_expression)[0]
            except:
                return
        fields = ['subregion', 'region', 'region__country', 'country']
        data = {getattr(obj, key).__class__.__name__: {x: getattr(getattr(obj, key), x) for x in ['id', 'name']}
                for key in fields if hasattr(obj, key)}
        if not data.get('name'):
            # Is geo coord search
            data['city'] = {'id': obj.pk, 'name': obj.name}
        # TODO: en la web de Django cities se muestra cómo obtener el código postal en función a la distancia.
        # No obstante, es bastante lento. Mientras lo  hago por el nombre, aunque habría que encontrar una
        # forma más fiable de hacer esto.
        postal_codes = PostalCode.objects.filter(name=obj.name)
        data['postal_code'] = postal_codes.first().code if postal_codes.count() else None
        if hasattr(obj, 'location'):
            data['coords'] = obj.location.coords
        return data
