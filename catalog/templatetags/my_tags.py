from django import template

register = template.Library()


# @register.filter()
# def media_filter(path):
#     """
#     Функция media_filter предназначена
#     для добавления префикса "media/" к пути файла.
#     """
#     if path:
#         return f"media/{path}"
#     return "#"


@register.filter(name='has_perm')
def has_perm(user, perm_name):
    """
    Проверяет, имеет ли пользователь указанное разрешение.
    Использование: {% if user|has_perm:"app_label.permission_codename" %}
    """
    return user.has_perm(perm_name)