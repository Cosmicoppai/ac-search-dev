from django.db import models
from itertools import chain
from django.utils.functional import keep_lazy
from django.utils.timezone import now


class CommentManager(models.Manager):
    def __init__(self):
        super(CommentManager, self).__init__()
        self.query = "SELECT comment_id, post_id, username, text, upvotes, create_date, delete_date" \
                     " FROM app_comment WHERE ts @@ websearch_to_tsquery('english', %s) AND sub=%s LIMIT 10000"


    def search(self, search_text, sub):
        return self.raw(self.query, (search_text, sub))


class Comment(models.Model):
    comment_id = models.CharField(max_length=32, verbose_name='comment id', unique=True, primary_key=True)
    post_id = models.CharField(max_length=32, verbose_name='post id')
    sub = models.CharField(max_length=32, verbose_name='Subreddit', default='cryptocurrency')
    username = models.CharField(max_length=60, verbose_name='username of the redditor')
    text = models.TextField(max_length=10000)
    upvotes = models.IntegerField(default=0, verbose_name='no of upvotes')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='date on which comment is created')
    delete_date = models.DateTimeField(verbose_name='date on which comment is deleted')

    class Meta:
        verbose_name_plural = "Comment's"
        get_latest_by = ['-create_date']

    def __str__(self):
        return f"{self.sub} -   {self.username}   -   {self.text}"

    objects = CommentManager()


class PostManager(models.Manager):
    def __init__(self):
        super(PostManager, self).__init__()
        self.query = "SELECT post_id, username, title, text, upvotes, image_url, create_date, delete_date" \
                     " FROM app_post WHERE ts @@ websearch_to_tsquery('english', %s) AND sub=%s LIMIT 10000"

    def search(self, search_text, sub):
        return self.raw(self.query, (search_text,sub))



class Post(models.Model):
    post_id = models.CharField(max_length=32, verbose_name='post id', primary_key=True, unique=True)
    sub = models.CharField(max_length=32, verbose_name='Subreddit', default='cryptocurrency')
    username = models.CharField(max_length=60)
    title = models.CharField(max_length=512)
    text = models.TextField(max_length=10000)
    upvotes = models.IntegerField(default=0, verbose_name='no of upvotes')
    image_url = models.URLField(blank=True, null=True, verbose_name="post image url")  # default max_length of 200 is used
    create_date = models.DateTimeField(default=now, verbose_name='date on which post is created')
    delete_date = models.DateTimeField(verbose_name='date on which post is deleted')

    class Meta:
        verbose_name_plural = "Post's"
        get_latest_by = ['-create_date']

    def __str__(self):
        return f"{self.sub} -   {self.username}   -   {self.title}"

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
        qs = sorted(queryset_chain, key=lambda instance: instance.delete_date)
        return qs