import csv
import os
from .models import Post

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
final_path = os.path.join(BASE_DIR, 'fixtures/one-million-reddit-confessions.csv')


def create_dummy_data():
    with open(final_path, mode='r', encoding='utf8', errors='ignore') as csv_file:
        data = csv.DictReader(csv_file)
        for obj in data:
            try:
                if obj['selftext'] == '[deleted]' or obj['selftext'] == '[removed]':
                    continue
                Post.objects.create(post_id=obj['id'], title=obj['title'], text=obj['selftext'],
                                username='ShadowGuy', upvotes=obj['score'])
            except ValueError or KeyError:
                pass
