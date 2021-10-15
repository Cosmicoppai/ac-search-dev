from django.views import generic
from .models import Post, Search
from django.http import HttpResponse, JsonResponse
from .db_init import create_dummy_data
from .paginator import Paginator
from .serializers import Serializer
from django.db import connection


class HomeView(generic.TemplateView):
    template_name = "app.html"


class SearchView(generic.ListView):
    paginate_by = 4
    count = 0
    paginate_orphans = 1

    def get(self, *args, **kwargs):
        qs = self.get_queryset()
        page_size = self.get_paginate_by(qs)
        """
        query_dict = self.check_query()
        if query_dict:
            page_num = self.request.GET.get('page', 1)
            paginate = Paginator(per_page=self.paginate_by, orphans=self.paginate_orphans, query_dict)
            total_result = paginate.count()
            if total_result:
                page, qs = paginate.get_page(page_num)
                previous = page.previous_page_number() if page.has_previous() else None
                next = page.next_page_number() if page.has_next() else None
                self.count = total_result
        else:
            qs, previous, next = [None], None, None
        data = Serializer(queryset).serialize()
        return JsonResponse({'count': self.count, 'previous': previous, 'next': next, 'data': data})
        
        """
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(qs, page_size)
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
            if _filter is not None and _filter != '' and _sub:
                qs = Search(query=_query, filter=_filter, sub=_sub).search_text()
                self.count = len(qs)
                return qs
        return Post.objects.none()

    """
    def check_query(self):
         _query = self.request.GET.get('q')
        _filter = self.request.GET.get('f', None)
        _sub = self.request.GET.get('sub', None)
        if _query is not None and _query != '':
            if _filter is not None and _filter != '' and _sub:
                return {'query':_query, 'filter':_filter,'sub':_sub}
        return None
    
    """


def test(requests):
    create_dummy_data()
    return HttpResponse("<h1>Successfully created dummy data</h1>")