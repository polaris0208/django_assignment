from django import forms
from .models import Products, Comment

class ProductsForm(forms.ModelForm):
  class Meta:
    model = Products
    fields = "__all__"
    exclude = ('author', 'like_user', 'hashtags')

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'
    exclude = ('products', 'user', 'product_name')