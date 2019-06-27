from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    keys = request.session.keys()
    if '' not in keys:
        request.session.pop('reviewed_products', [])

    reviews = request.session.get('reviewed_products', [])
    is_review_exist = True
    if pk in reviews:
        is_review_exist = False


    form = ReviewForm
    if request.method == 'POST':
        product = pk
        request.session.modified = True
        reviews = reviews.append(product)
        request.session['reviewed_products'] = reviews
        form = ReviewForm(
            {'text': request.POST['text']}
        )
        if form.is_valid():
            filled_form = form.save(commit=False)
            filled_form.product_id = product
            form.save()
            return redirect('product_detail', pk=product)

    context = {
        'form': form,
        'is_review_exist': is_review_exist,
        'product': product
    }

    return render(request, template, context)
