from django.db.models import Count

from .models import *

menu = [{'title': "About site", 'url_name': 'about'},
        {'title': "Add article", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        {'title': "Login", 'url_name': 'login'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['categories'] = categories
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context
