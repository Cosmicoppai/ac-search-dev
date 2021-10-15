from django.db import models
from itertools import chain
from django.db import connection

"""
def dictfetchall(cursor):
    
    # Convert the list result from db into dict
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()]


class CommentSearch:
    def __init__(self, search_text):
        self.query = "SELECT DISTINCT id, sub, author, text, date FROM app_comment WHERE UPPER(text) LIKE UPPER(%s) ORDER BY date DESC"
        self.search_text = search_text


    def search(self):
        if self.search_text is not None:
            with connection.cursor() as cursor:
                cursor.execute(self.query, [self.search_text])
                return dictfetchall(cursor)

"""


class CommentManager(models.Manager):
    def __init__(self):
        super(CommentManager, self).__init__()
        self.query = "SELECT DISTINCT comment_id, post_id, sub, username, text, date FROM app_comment WHERE UPPER(text) LIKE UPPER(%s) AND sub=%s ORDER BY date DESC"


    def search(self, search_text, sub):
        result = self.raw(self.query, (f'%{search_text}%', sub))
        return result


class Comment(models.Model):
    comment_id = models.CharField(max_length=32, verbose_name='comment id', unique=True, primary_key=True)
    post_id = models.CharField(max_length=32, verbose_name='post id')
    sub = models.CharField(max_length=32, verbose_name='Subreddit', default='cryptocurrency')
    username = models.CharField(max_length=60)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Comment's"
        get_latest_by = ['-date']

    def __str__(self):
        return f"{self.sub} -   {self.username}   -   {self.text}"

    """
    @staticmethod
    def search(search_text=None):
        comment_search = CommentSearch(search_text)
        return comment_search.search()
        """

    objects = CommentManager()


"""
class PostSearch:
    def __init__(self, search_text):
        self.query = 'SELECT DISTINCT id, sub, author, title, text, date FROM app_post WHERE (UPPER(%s) LIKE UPPER(title) OR UPPER(text) LIKE UPPER(%s)) ORDER BY date DESC'
        self.search_text = search_text

    def search(self):
        with connection.cursor() as cursor:
            cursor.execute(self.query, [self.search_text, self.search_text])
            return dictfetchall(cursor)

"""


class PostManager(models.Manager):
    def __init__(self):
        super(PostManager, self).__init__()
        self.query = "SELECT DISTINCT post_id, sub, username, title, text, date FROM app_post WHERE (UPPER(title) LIKE UPPER(%s) OR UPPER(text) LIKE UPPER(%s)) AND sub=%s ORDER BY date DESC"

    def search(self, search_text, sub):
        result = self.raw(self.query, (f'%{search_text}%', f'%{search_text}%', sub))
        return result



class Post(models.Model):
    post_id = models.CharField(max_length=32, verbose_name='post id', primary_key=True, unique=True)
    sub = models.CharField(max_length=32, verbose_name='Subreddit', default='cryptocurrency')
    username = models.CharField(max_length=60)
    title = models.CharField(max_length=512)
    text = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Post's"
        get_latest_by = ['-date']

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

    def search_text(self):
        if self.filter == 'p':  # if filter is p(posts)
            self.post_result = Post.objects.search(self.query, self.sub)
        elif self.filter == 'c':  # if filter is c(comments)
            self.comment_result = Comment.objects.search(self.query, self.sub)
        elif self.filter == 'pc':  # if filter is pc(posts and comments)
            self.post_result = Post.objects.search(self.query, self.sub)
            self.comment_result = Comment.objects.search(self.query, self.sub)
        queryset_chain = chain(self.post_result, self.comment_result)
        qs = sorted(queryset_chain, key=lambda instance: instance.date, reverse=True)
        return qs