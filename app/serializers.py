from .models import Post, Comment


class Serializer:
    def __init__(self, queryset):
        self.queryset = queryset
        self.result = []

    def serialize(self):
        for item in self.queryset:
            if item.__class__.__name__ == 'Post':
                self.result.append(
                    dict(type='post', post_id=item.post_id,
                         title=item.title, text=item.text,
                         upvotes=item.upvotes, image_url=item.image_url, username=item.username, date=item.date))
            else:
                self.result.append(
                    dict(type='comment', post_id=item.post_id,
                         comment_id=item.comment_id,
                         text=item.text, upvotes=item.upvotes, username=item.username,
                         date=item.date))
        return self.result