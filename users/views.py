from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from products.models import Products

def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {
        "member": member,
        'follower_count': member.follower_counter,  # 팔로워 수
        'following_count': member.following_counter,
        'liked_products' : Products.objects.filter(like_user=member)
        }
    return render(request, "users/profile.html", context)

@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect('users:profile', username=member.username)
    else:
        return redirect("accounts:login")
