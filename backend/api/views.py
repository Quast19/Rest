from django.shortcuts import render
from django.http import JsonResponse
import json

from products.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()    
    data= {}
    if model_data:
        data['id'] = model_data.id
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
# # The previous functions explaining somethings
#     # request is a instance of httprequest class, provided by django framework, not the same as python request
#     #flow = basic.py ->requested this function, before returning we printed the json data and returned our json data
#     print(request.body)
#     body = request.body
#     data = {}
#     #data['message'] = "Hi there this is your django api response"
#     try:
#         data = json.loads(body) #json data to python dictionary, we put it in try block because if body has no json then we can come across error
#     except:
#         pass
#     print(data.keys())
#     data['headers'] = dict(request.headers)
#     data['content_type'] = request.content_type
#     print(request.headers)
#     #return JsonResponse({"message:":" Hi there this is your django api response "})
#     return JsonResponse(data)
# # Create your views here.
    return JsonResponse(data)
