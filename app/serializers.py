from .models import Post, Comment


class Serializer:
    def __init__(self, queryset):
        self.queryset = queryset
        self.result = []

    def serialize(self):
        for item in self.queryset:
            obj = {}
            if item.__class__.__name__ == 'Post':
                obj['type'] = 'post'
                obj['post_id'] = item.post_id
                obj['title'] = item.title
                obj['text'] = item.text
                obj['username'] = item.username
                obj['date'] = item.date
                self.result.append(obj)
            else:
                obj['type'] = 'comment'
                obj['post_id'] = item.post_id
                obj['comment_id'] = item.comment_id
                obj['text'] = item.text
                obj['username'] = item.username
                obj['date'] = item.date
                self.result.append(obj)
        return self.result


