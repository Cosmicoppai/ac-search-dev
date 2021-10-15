from .models import Post, Comment

titles = ['What is Lorem Ipsum?',
          'Why do we use it?',
          'Where does it come from?',
          'Where can I get some?',
          'The standard Lorem Ipsum passage, used since the 1500s',
          'Bitcoin']

posts = [
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.Why do we use it?It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."
    ,
    "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."
    ,
    "Bitcoin は、2008年にサトシ・ナカモトという名前を使った無名の人物またはグループによって発明された、Peer to Peer型の暗号通貨である。この通貨は、その実装がオープンソースソフトウェアとして公開され、2009年に使用が開始された。"
]

post_ids = ['p13kjw', 'p23kjw', 'p33kjw', 'p43kjw', 'p53kjw', 'p63kjw']
comment_ids = ['h91hamgl', 'h2hamgl', 'h3hamgl']


def create_dummy_data():
    for i in range(len(titles)):
        Post.objects.create(post_id=post_ids[i], title=titles[i], text=posts[0], author='dio')

    for j in range(len(posts)):
        Comment.objects.create(comment_id=comment_ids[j],  post_id='p13kjw', text=posts[j], author='martin')