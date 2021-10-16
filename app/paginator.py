from .models import Search
from django.utils.functional import cached_property
from django.core.paginator import PageNotAnInteger, InvalidPage, EmptyPage
from math import ceil


class Paginator:
    def __init__(self, queryset, per_page, orphans=0, total_result=0):
        self.queryset = queryset
        self.per_page = per_page
        self.orphans = orphans
        self.total_result = total_result

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
        if top + self.orphans >= self.total_result:
            top = self.total_result
        return Page(page_num, self), self.queryset[bottom:top]  # limit the search from bottom to top

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.total_result == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.total_result - self.orphans)
        return ceil(hits / self.per_page)


class Page:

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