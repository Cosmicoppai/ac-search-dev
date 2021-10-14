from django.views import generic
from .models import Post, Search
from django.http import HttpResponse
from .db_init import create_dummy_data
from django.contrib.postgres.search import SearchVector
from django.db.models import Q


class HomeView(generic.TemplateView):
    template_name = "app.html"


class SearchView(generic.ListView):
    template_name = 'app.html'
    paginate_by = 10
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('search')
        context['sub'] = self.request.GET.get('sub', 'cryptocurrency')
        return context

    def get_queryset(self):
        _query = self.request.GET.get('search')
        _filter1 = self.request.GET.get('filter1', None)
        _filter2 = self.request.GET.get('filter2', None)
        if _query is not None and _query != '':
            if _filter1 is not None or _filter2 is not None and _filter1 != _filter2:
                # print(Post.objects.filter(text__search=_query).explain(analyze=True))
                # print(Post.objects.filter(Q(text__icontains=_query), Q(title__icontains=_query)).explain(analyze=True))
                # print(Post.objects.annotate(search=SearchVector('title', 'text'), ).filter(search=_query).explain(analyze=True))
                qs = Search(query=_query, filter1=_filter1, filter2=_filter2).search_text()
                self.count = len(qs)
                return qs
        return Post.objects.none()


def test(requests):
    create_dummy_data()
    return HttpResponse("<h1>Successfully created dummy data</h1>")
