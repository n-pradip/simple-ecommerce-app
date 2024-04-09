from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from main.models import ProductModel, Like
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    products_list = ProductModel.objects.all().order_by("-like_count")[:4]
    context = {
        'product_list': products_list,
    }
    return render(request, 'main/homepage.html', context)

@login_required
def product_list(request):
    products = ProductModel.objects.all()
    return render(request, 'main/product_list.html', {'products': products})

@login_required
def product_detail_view(request, product_id):
    product = get_object_or_404(ProductModel, pk=product_id)
    user = request.user
    has_liked = False
    if user.is_authenticated:
        has_liked = Like.objects.filter(user=user, product=product).exists()
    return render(request, 'main/product_detail.html', {'product': product, 'has_liked': has_liked})

@login_required
def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = ProductModel.objects.filter(name__icontains=query)
    return render(request, 'main/search_results.html', {'results': results, 'query': query})

# def like_product(request, product_id):
#     print("hrllo")
#     if request.method == 'POST':
#         product = get_object_or_404(ProductModel, pk=product_id)
#         print(f'======{product}')
#         user = request.user
#         print(f'========={user}')
#         if not user.is_authenticated:
#             return JsonResponse({'error': 'User is not authenticated'}, status=401)
#         if not Like.objects.filter(user=user, product=product).exists():
#             Like.objects.create(user=user, product=product)
#             product.like_count += 1
#             product.save()
#             print(f"========={product.like_count}")
#             return JsonResponse({'like_count': product.like_count})
#         else:
#             return JsonResponse({'error': 'You have already liked this product'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
def like_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(ProductModel, pk=product_id)
        user = request.user
        if user.is_authenticated:
            if not Like.objects.filter(user=user, product=product).exists():
                Like.objects.create(user=user, product=product)
                product.like_count += 1
                product.save()
                return redirect(reverse('home')) 
            else:
                # User has already liked the product, redirect back to product detail page
                return redirect(reverse('product_detail', args=[product_id]))
        else:
            # User is not authenticated, you may want to redirect to a login page or show an error message
            return redirect(reverse('login'))  # Redirect to login page, change 'login' to your actual login URL name
    else:
        # Handle other HTTP methods if necessary
        return redirect(reverse('home')) 