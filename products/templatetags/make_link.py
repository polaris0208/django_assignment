from django import template

register = template.Library()

@register.filter
def hashtag_link(hashtag):
    tag_link = f'<a href="/products/{hashtag.pk}/hashtag/">{hashtag.name}</a>'
    return tag_link
