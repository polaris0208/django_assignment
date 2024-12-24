from django import forms
from .models import Products, Comment, HashTag


class ProductsForm(forms.ModelForm):
    hashtags_str = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Products
        fields = "__all__"
        exclude = ("author", "like_user", "views", "hashtags")

    def save(self, commit=True):
        product = super().save(commit=False)

        if self.user:
            product.user = self.user
            product.author = self.user

        if commit:
            product.save()

        hashtags_input = self.cleaned_data.get("hashtags_str", "")
        hashtag_list = [h for h in hashtags_input.replace(",", " ").split() if h]
        new_hashtags = []
        for ht in hashtag_list:
            ht_obj, created = HashTag.objects.get_or_create(name=ht)
            new_hashtags.append(ht_obj)
        product.hashtags.set(new_hashtags)

        if not commit:
            product.save()

        return product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ("products", "user", "product_name")
