from django import template


register = template.Library()


@register.inclusion_tag("user/tags/avatar_img.html")
def user_avatar(user, classes=None, style=None):  # 到时候要把这个改下，参数太多了
    """返回用户头像，img标签。如果用户avatar字段不为空，则返回用户头像地址，为空则返回默认头像"""
    return{"user": user, "style": style, "classes": classes}
