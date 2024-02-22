from config import app, api
from models import Post, Comment
from flask_restful import Resource


# create routes here:
class SortedPosts(Resource):
    def get(self):
        posts = [post.to_dict() for post in Post.query.all()]
        sorted_posts = sorted(posts, key=lambda post: post["title"])
        return sorted_posts, 200


class PostsByAuthor(Resource):
    def get(self, name):
        posts = [
            post.to_dict() for post in Post.query.filter(Post.author == name).all()
        ]
        return posts, 200


api.add_resource(SortedPosts, "/api/sorted_posts")
api.add_resource(PostsByAuthor, "/api/posts_by_author/<author_name>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
