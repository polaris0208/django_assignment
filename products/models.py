from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import re


def products_image_path(instance, filename):
    return f"products/{instance.user.username}/{filename}"


def validation_hashtag(value):
    if not re.match(r"^[0-9a-zA-Z_]+$", value):
        # ^: 시작 / $ : 특정 패턴 끝
        raise ValidationError


class HashTag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validation_hashtag])

    def __str__(self):
        return f"#{self.name}"


class Products(models.Model):
    # 제목
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 상품 설명
    product_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to=products_image_path, blank=True, null=True)
    # 좋아요/찜
    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="like_products",
        blank=True
    )

    # 해쉬태그
    hashtags = models.ManyToManyField(HashTag, related_name='products', blank=True)
    # 조회수
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    @property
    def like_user_counter(self):
        return self.like_user.count()
    
    def view_counter(self):
        self.views = self.views + 1
        self.save()
        return self.views


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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return self.content
