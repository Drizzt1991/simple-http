
from webob import Request, Response
from webob.exc import HTTPNotFound, HTTPFound
import re
from sqlalchemy import create_engine, text as sql_text


engine = create_engine('mysql+mysqlconnector://root@localhost/blog')


class Route:

    pattern = ""
    layout = """
<html>
    <head>
        <script type="text/javascript">
        </script>
        <title>{title}</title>
    </head>
    <body>
        <header>
            <h1>{title}</h1>
        </header>
        <section>
            {body}
        </section>
        <footer>
            Made by Taras Voinarovskyi. All rights reversed %).
        </footer>
    </body>
</html>
    """

    def __init__(self):
        pass

    def match(self, path):
        return re.compile(self.pattern).match(path)

class ViewPost(Route):

    pattern = "^/post/(\d+)$"

    def handle(self, request, post_id):
        res = Response()

        post_id = int(post_id)
        cursor = engine.execute("""
            SELECT text, title
            FROM blogs
            WHERE id={post_id}
            """.format(post_id=post_id))
        post = cursor.fetchone()
        if post is None:
            return HTTPNotFound()

        res.text = self.layout.format(
            body=post.text,
            title=post.title
        )
        return res


class EditPost(Route):

    pattern = "^/post/(\d+)/edit$"


    def handle(self, request, post_id):
        res = Response()
        if request.method == "POST":
            title = request.POST['title']
            text = request.POST['text']
            cursor = engine.execute(sql_text("""
                UPDATE blogs
                SET text=:text, title=:title
                WHERE id=:post_id
                """), 
                post_id=post_id,
                text=text,
                title=title
                )
            return HTTPFound(location="/post/{}".format(post_id))
        res.text = self.layout.format(
            title="Edit Post {}".format(post_id),
            body="""
<form action="" method="POST">
    <input type="text" name="text" />
    <input type="text" name="title" />
    <input type="SUBMIT" name="Submit" value="Submit" />
</form>
            """.format()
        )
        return res


class PostList(Route):

    pattern = "^/post/$"


    def handle(self, request):
        res = Response()
        res.text = self.layout.format(
            body="Post List"
        )
        return res


class PostSearch(Route):

    pattern = "^/post/search$"


    def handle(self, request):
        res = Response()
        res.text = self.layout.format(
            body="Post Search"
        )
        return res


routes = [
    ViewPost(),
    PostSearch(),
    PostList(),
    EditPost()
]

# Every WSGI application must have an application object - a callable
# object that accepts two arguments. For that purpose, we're going to
# use a function (note that you're not limited to a function, you can
# use a class for example). The first argument passed to the function
# is a dictionary containing CGI-style envrironment variables and the
# second variable is the callable object (see PEP 333).
def app(environ, start_response):
    req = Request(environ)

    for route in routes:
        match = route.match(req.path)
        if match:
            res = route.handle(req, *match.groups())
            break
    else:
        res = HTTPNotFound()

    return res(environ, start_response)
