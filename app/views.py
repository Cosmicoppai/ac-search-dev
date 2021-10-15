from django.views import generic
from .models import Post, Search
from django.http import HttpResponse, JsonResponse
from .db_init import create_dummy_data
from .serializers import Serializer


class HomeView(generic.TemplateView):
    template_name = "app.html"


class SearchView(generic.ListView):
    paginate_by = 12
    count = 0

    def get(self, *args, **kwargs):
        qs = self.get_queryset()
        page_size = self.get_paginate_by(qs)
        if page_size:
            # edited the paginate_queryset in MultipleObjectMixin in list.py to return only page and queryset
            page, queryset = self.paginate_queryset(qs, page_size)
            previous = page.previous_page_number() if page.has_previous() else None
            next = page.next_page_number() if page.has_next() else None
        else:
            previous, next = None, None
            queryset = qs
        data = Serializer(queryset).serialize()
        return JsonResponse({'count': self.count, 'previous': previous, 'next': next, 'data': data})

    def get_queryset(self):
        _query = self.request.GET.get('q')
        _filter = self.request.GET.get('f', None)
        _sub = self.request.GET.get('sub', None)
        if _query is not None and _query != '':
            if _filter is not None and _filter != '':
                qs = Search(query=_query, filter=_filter, sub=_sub).search_text()
                self.count = len(qs)
                return qs
        return Post.objects.none()


def test(requests):
    create_dummy_data()
    return HttpResponse("<h1>Successfully created dummy data</h1>")