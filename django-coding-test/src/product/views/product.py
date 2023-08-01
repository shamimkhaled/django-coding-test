from django.views import generic
from django.shortcuts import render
from product.models import Variant, ProductVariant, Product, ProductVariantPrice
from django.shortcuts import get_object_or_404
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import ensure_csrf_cookie


# Create Product View
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'
    #form_class = CreateProductForm
    model = Product
    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        
        context['product'] = True 
        context['variants'] = list(variants.all())
        return context
    
    
    @csrf_exempt
    #@csrf_protect  
    #@method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        try:
            # Get the data from the POST request
            product_name = request.POST.get('product_name')
            if not product_name:
                return JsonResponse({'error': 'Product name is required.'}, status=400)

            product_sku = request.POST.get('product_sku')
            description = request.POST.get('description')
            images = request.FILES.getlist('images')  # Assuming the images are sent as files
            variant_data = request.POST.getlist('product_variant[]')  # Assuming the selected variants are sent as a list
            product_variant_prices = request.POST.getlist('product_variant_prices[]')  # Assuming the selected variants are sent as a list

            # Create the product instance
            product = Product.objects.create(
                title=product_name,
                sku=product_sku,
                description=description
            )

            # Save the images to the product instance (assuming you have a field in the Product model to store images)
            for image in images:
                product.images.add(image)

            # Create the product variant instances
            for variant_item in variant_data:
                option_id, *tags = variant_item.split('/')  
                option = Variant.objects.get(pk=option_id)
                product_variant = ProductVariant.objects.create(
                    product=product,
                    variant_title=option.title,  
                )
                product_variant.tags.set(tags)

            # Create the product variant price instances
            for price_item in product_variant_prices:
                variant_id, price, stock = price_item.split('/')  
                variant = ProductVariant.objects.get(pk=variant_id)
                product_variant_price = ProductVariantPrice.objects.create(
                    product_variant=variant,
                    price=float(price),
                    stock=float(stock),
                    product=product
                )
                product_variant_price.tags.set(tags)

            
            return JsonResponse({'message': 'Product created successfully'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)








class ListViewProductTable(generic.TemplateView):  
      #model = ProductVariant      
     template_name = 'products/list.html'
      #context_object_name = 'products'
     def get_context_data(self, **kwargs):
        context = super(ListViewProductTable, self).get_context_data(**kwargs)
        variants = ProductVariant.objects.filter().values('variant_id', 'variant_title')
        #context['products'] = True
        context['variants'] = list(variants.all())
        return context


     def get_queryset(self, request):
        title = Product.objects.filter(title__icontains='title')
        template = loader.get_template('products/list.html')
        context = {
            'title': title,
        }
        return HttpResponse(template.render(context, request))


      
   





     
# def search(request):
#         if 'keyword' in request.GET:
#             keyword = request.GET['keyword']
#             if keyword:
#                 products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
#                 product_count = products.count()
#         context = {
#             'products': products,
#             'product_count': product_count,
#         }
#         return render(request, 'products/list.html', context)
     

#   # Fetch form input values from the request.GET dictionary
#         title = self.request.GET.get('title')
#         variant = self.request.GET.get('variant')
#         price_from = self.request.GET.get('price_from')
#         price_to = self.request.GET.get('price_to')
#         date = self.request.GET.get('date')

#         # Query products and apply filters based on form inputs
#         products = Product.objects.all()

#         if title:
#             products = products.filter(Q(title__icontains=title))

#         if variant:
#             products = products.filter(Q(variant__variant_title__icontains=variant))

#         if price_from:
#             products = products.filter(Q(price__gte=price_from))

#         if price_to:
#             products = products.filter(Q(price__lte=price_to))

#         if date:
#             products = products.filter(Q(created_date__date=date))

#         # Pass the filtered products to the template
#         context['products'] = products

#         context['variants'] = list(variants.all())
#         return context