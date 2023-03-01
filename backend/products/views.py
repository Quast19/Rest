from rest_framework import generics, mixins, permissions, authentication
from .models import Product
from .serializers import ProductSerializer
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


########################## IMPORTS ##################################################################
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    
    permission_classes = [permissions.DjangoModelPermissions]
    def perform_create(self, serializer):
        # serializer.save(user = self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content = content)
    
product_list_create_view =ProductListCreateAPIView.as_view()


class ProductDetailAPIview(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
product_detail_view = ProductDetailAPIview.as_view()

class ProductUpdateAPIview(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title   
product_update_view = ProductUpdateAPIview.as_view()

class ProductDestroyAPIview(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
            
        
        
product_delete_view = ProductDestroyAPIview.as_view()


class ProductListAPIview(generics.ListAPIView):
    '''
    Not Gonna use this method
    '''
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
product_list_view = ProductListAPIview.as_view()

class ProductMixinView(
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
    mixins.DestroyModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field= 'pk'
    
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)   
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
product_mixin_view = ProductMixinView.as_view()




















@api_view(["GET", "POST"])
def product_alt_view(request,pk= None ,*args, **kwargs):
    method = request.method
    
    
    if method == "GET":
        #can be detail or list view now, so we need to differ with help of primary key.
        if pk is not None:
            #detail view
            obj = get_object_or_404(Product, pk = pk)
            data = ProductSerializer(obj, many = False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many = True).data
        return Response(data)
    if method== "POST":
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):#for robust message use raise_exception
            #print(serializer.validated_data)
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content = content)
            return Response(serializer.data)
        return Response({"invalid":"not good data, or in serializable data"}, status = 400)