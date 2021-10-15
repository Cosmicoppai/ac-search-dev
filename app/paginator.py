from .models import Search
from django.utils.functional import cached_property
import collections.abc


class Paginator:
    def __init__(self, per_page, orphans=0, **kwargs):
        self.per_page = per_page
        self.orphans = orphans
        # self.query = kwargs['query']
        # self.filter = kwargs['filter']
        # self.sub = kwargs['sub']
        self.search = Search(query=kwargs['query'], filter=kwargs['filter'], sub=kwargs['sub'])

    def validate_number(self, page_num):
        try:
            if isinstance(page_num, float) and not page_num.is_integer():
                raise ValueError
            page_num = int(page_num)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if page_num < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if page_num > self.num_pages:
            if page_num == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage(_('That page contains no results'))
        return page_num

    def get_page(self, page_num):
        try:
            page_num = self.validate_number(page_num)
        except PageNotAnInteger:
            page_num = self.num_pages if page_num == 'last' else 1
        except EmptyPage:
            page_num = self.num_pages
        return self.page(page_num)

    def page(self, page_num):
        bottom = (page_num - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(page_num, self), self.search.search_text(bottom, top)  # limit the search from bottom to top

    @cached_property
    def count(self):
        # will return the total no of result
        return self.search.count_result()

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.count - self.orphans)
        return ceil(hits / self.per_page)


class Page(collections.abc.Sequence):

    def __init__(self,  page_number, paginator):
        self.page_number = page_number
        self.paginator = paginator

    def has_next(self):
        return self.page_number < self.paginator.num_pages

    def has_previous(self):
        return self.page_number > 1

    def next_page_number(self):
        return self.paginator.validate_number(self.page_number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.page_number - 1)