from django.db import models
from django.conf import settings


class Products(models.Model):
    # 제목
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 상품 설명
    product_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images/", blank=True)  # 비어있어도 된다
    # 좋아요/찜
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="like_products",
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    products = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="comments"
    )
    # CASCADE 참조하는 데이터가 삭제되면 같이 삭제
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.content
