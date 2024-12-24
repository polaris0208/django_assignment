from django.db import models
from django.contrib.auth.models import AbstractUser

def user_profile_image_path(instance, filename):
    return f"profile/{instance.username}/{filename}"


class User(AbstractUser):
    profile_image = models.ImageField(
        default='profile/default.png',
        upload_to=user_profile_image_path, blank=True, null=True
    )
    following = models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
        blank=True,
    )  # symmetrical 대칭 기능

    @property
    def follower_counter(self):
        return self.followers.count()  # 역참조 해서 확인 / 나를 팔로우

    @property
    def following_counter(self):
        return self.following.count()  # 정참조 해서 확인 / 내가 팔로우

    def __str__(self):
        return self.username
