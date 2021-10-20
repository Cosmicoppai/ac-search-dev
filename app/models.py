from django.db import models
from itertools import chain
from django.db.models import Q
# from django.db import connection
from django.utils.functional import cached_property, keep_lazy
from django.utils.timezone import now


class CommentManager(models.Manager):
    def __init__(self):
        super(CommentManager, self).__init__()
        self.query = "SELECT DISTINCT comment_id, post_id, sub, username, text, upvotes, create_date, delete_date FROM app_comment " \
                     "WHERE UPPER(text) LIKE UPPER(%s) AND sub=%s ORDER BY create_date DESC"


    def search(self, search_text, sub):
        result = self.raw(self.query, (f'%{search_text}%', sub))
        return result

    def count_result(self, search_text, sub):
        count = self.filter(Q(text__icontains=search_text),
                            Q(sub__iexact=sub)).count()
        return count


class Comment(models.Model):
    comment_id = models.CharField(max_length=32, verbose_name='comment id', unique=True, primary_key=True)
    post_id = models.CharField(max_length=32, verbose_name='post id')
    sub = models.CharField(max_length=32, verbose_name='Subreddit', default='cryptocurrency')
    username = models.CharField(max_length=60, verbose_name='username of the redditor')
    text = models.TextField(max_length=10000)
    upvotes = models.IntegerField(default=0, verbose_name='no of upvotes')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='date on which comment is created')
    delete_date = models.DateTimeField(blank=True, null=True, verbose_name='date on which comment is deleted')

    class Meta:
        ordering = ['-create_date']
        verbose_name_plural = "Comment's"
        get_latest_by = ['-create_date']

    def __str__(self):
        return f"{self.sub} -   {self.username}   -   {self.text}"

    """
    @staticmethod
    def search(search_text=None):
        comment_search = CommentSearch(search_text)
        return comment_search.search()
        """

    objects = CommentManager()



class PostManager(models.Manager):
    def __init__(self):
        super(PostManager, self).__init__()
        self.query = "SELECT DISTINCT post_id, sub, username, title, text, upvotes, image_url, " \
                     "create_date, delete_date FROM app_post WHERE (UPPER(title) LIKE UPPER(%s) OR " \
                     "UPPER(text) LIKE UPPER(%s)) AND sub=%s ORDER BY create_date DESC"

    def search(self, search_text, sub):
        result = self.raw(self.query, (f'%{search_text}%', f'%{search_text}%', sub))
        return result

    def count_result(self, search_text, sub):
        count = self.filter(Q(title__icontains=search_text) | Q(text__icontains=search_text), Q(sub__iexact=sub)).count()
        return count



class Post(models.Model):
    post_id = models.CharField(max_length=32, verbose_name='post id', primary_key=True, unique=True)
    sub = models.CharField(max_length=32, verbose_name='Subreddit', default='cryptocurrency')
    username = models.CharField(max_length=60)
    title = models.CharField(max_length=512)
    text = models.TextField(max_length=10000)
    upvotes = models.IntegerField(default=0, verbose_name='no of upvotes')
    image_url = models.URLField(blank=True, null=True, verbose_name="post image url")  # default max_length of 200 is used
    create_date = models.DateTimeField(default=now, verbose_name='date on which post is created')
    delete_date = models.DateTimeField(blank=True, null=True, verbose_name='date on which post is deleted')

    class Meta:
        ordering = ['-create_date']
        verbose_name_plural = "Post's"
        get_latest_by = ['-create_date']

    def __str__(self):
        return f"{self.sub} -   {self.username}   -   {self.title}"

    """
    @staticmethod
    def search(search_text=None):
        post_search = PostSearch(search_text)
        return post_search.search()
        """

    objects = PostManager()


class Search:
    def __init__(self, query, filter=None, sub=None):
        self.filter = filter
        self.query = query
        self.sub = sub
        self.post_result = Post.objects.none()
        self.comment_result = Comment.objects.none()


    @keep_lazy(tuple)
    def search_text(self):
        if self.filter == 'p':  # if filter is p(posts)
            self.post_result = Post.objects.search(self.query, self.sub)
        elif self.filter == 'c':  # if filter is c(comments)
            self.comment_result = Comment.objects.search(self.query, self.sub)
        elif self.filter == 'pc':  # if filter is pc(posts and comments)
            self.post_result = Post.objects.search(self.query, self.sub)
            self.comment_result = Comment.objects.search(self.query, self.sub)
        queryset_chain = chain(self.post_result, self.comment_result)
        # sort the whole queryset in reverse (i.e new post will come first)
        qs = sorted(queryset_chain, key=lambda instance: instance.create_date, reverse=True)
        return qs

    """
    
    def get_model(self):
        if self.filter == 'p':  # if filter is p(posts)
            return Post, None
        if self.filter == 'c':  # if filter is c(comments)
            return None, Comment
        if self.filter == 'pc':  # if filter is pc(posts and comments)
            return Post, Comment

    @cached_property
    def count_result(self):
        total_no_of_results = 0
        _models = self.get_model()
        for model in _models:
            try:
                total_no_of_results += model.objects.count_result(self.query, self.sub)
            except AttributeError:
                pass
        return total_no_of_results
        """