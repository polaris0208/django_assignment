from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Comment, HashTag
from .forms import ProductsForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import FormView
from django.db.models import Q


def products(request):
    products = Products.objects.all().order_by("-created_at")
    context = {"products": products}
    return render(request, "products/products.html", context)


def detail(request, pk):
    products = get_object_or_404(Products, pk=pk)
    comment_form = CommentForm()
    comments = products.comments.all().order_by("-pk")
    context = {
        "products": products,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "products/detail.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            # return redirect("products:detail", products.pk)
            return redirect("products:products")
    else:
        form = ProductsForm()

    context = {"form": form}
    return render(request, "products/create.html", context)


@login_required
@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        products = get_object_or_404(Products, pk=pk)
        products.delete()
    return redirect("products:products")


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    products = get_object_or_404(Products, pk=pk)
    if request.method == "POST":
        form = ProductsForm(request.POST, instance=products)
        if form.is_valid():
            form.save()
            return redirect("products:detail", products.pk)
    else:
        form = ProductsForm(instance=products)

    context = {"form": form, "products": products}
    return render(request, "products/update.html", context)


@login_required
@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        products = get_object_or_404(Products, pk=pk)
        if products.like_user.filter(pk=request.user.pk).exists():
            products.like_user.remove(request.user)
        else:
            products.like_user.add(request.user)
        return redirect("products:products")
    else:
        return redirect("accounts:login")


@login_required
@require_POST
def comment_create(request, pk):
    products = get_object_or_404(Products, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.products = products
        comment.user = request.user
        comment.save()
        return redirect("products:detail", products.pk)


@login_required
@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("products:detail", pk)


@login_required
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(HashTag, pk=hash_pk)
    products = hashtag.products.order_by("-pk")
    context = {
        "hashtag": hashtag,
        "products": products,
    }
    return render(request, "products/hashtag.html", context)


class SearchFormView(FormView):
    form_class = SearchForm
    template_name = "products/search.html"

    def form_valid(self, form):
        searchWord = form.cleaned_data["search_word"]
        products_list = Products.objects.filter(
            Q(title__icontains=searchWord)
            | Q(product_name__icontains=searchWord)
            | Q(content__icontains=searchWord)
        ).distinct()

        context = {
            "form": form,
            "searchWord": searchWord,
            "products_list": products_list,
        }

        return render(self.request, "products/search.html", context)