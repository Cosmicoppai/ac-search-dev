from django.views import generic
from django.views.generic.base import View
from .models import Post, Search
from django.http import HttpResponse, JsonResponse
from .db_init import create_dummy_data
from .paginator import Paginator
from .serializers import Serializer


class HomeView(generic.TemplateView):
    template_name = "app.html"


class SearchView(generic.TemplateView):
    template_name = "app.html"



class SearchApi(View):
    paginate_by = 25
    count = 0
    paginate_orphans = 4

    def get(self, *args, **kwargs):
        page_num = self.request.GET.get('page', 1)
        qs = self.get_queryset()
        page, queryset = self.paginate(qs, page_num)  # paginate the queryset
        previous = page.previous_page_number() if page.has_previous() else None
        next = page.next_page_number() if page.has_next() else None
        data = Serializer(queryset).serialize()
        return JsonResponse({'count': self.count, 'prev': previous, 'next': next, 'data': data})

    def get_queryset(self):
        _query = self.request.GET.get('q')
        _filter = self.request.GET.get('f', None)
        _sub = self.request.GET.get('sub', None)
        if _query and _query != '':
            if _filter and _filter != '' and _sub:
                qs = Search(query=_query, filter=_filter, sub=_sub).search_text()
                self.count = len(qs)
                return qs
        return Post.objects.none()

    def paginate(self, queryset, page_num=1):
        paginator = Paginator(queryset, self.paginate_by, self.paginate_orphans, self.count)
        return paginator.get_page(page_num)



def test(request):
    create_dummy_data()
    return HttpResponse("<h1>Successfully created dummy data</h1>")