from config import app, api
from models import Post, Comment
from flask_restful import Resource


# create routes here:
class SortedPosts(Resource):
    def get(self):
        posts = [post.to_dict() for post in Post.query.all()]
        posts.sort(key=lambda post: post.get("title"))
        return posts, 200


class PostsByAuthor(Resource):
    def get(self, author_name):
        posts = [
            post.to_dict() for post in Post.query.filter_by(author=author_name.title())
        ]
        print([post["author"] for post in posts])
        return posts, 200


class SearchPosts(Resource):
    def get(self, title):
        posts = [
            post.to_dict() for post in Post.query.filter(Post.title.contains(title))
        ]
        return posts, 200


class PostsByComments(Resource):
    def get(self):
        posts = [post.to_dict() for post in Post.query.all()]
        posts.sort(key=lambda post: len(post.get("comments")), reverse=True)
        return posts, 200


class MostPopular(Resource):
    def get(self):
        counts = {}
        for comment in Comment.query.all():
            if comment.commenter in counts:
                counts[comment.commenter] += 1
            else:
                counts[comment.commenter] = 1
        max_commenter = max(counts, key=lambda commenter: counts[commenter])
        return {"commenter": max_commenter}, 200


api.add_resource(SortedPosts, "/api/sorted_posts")
api.add_resource(PostsByAuthor, "/api/posts_by_author/<author_name>")
api.add_resource(SearchPosts, "/api/search_posts/<title>")
api.add_resource(PostsByComments, "/api/posts_ordered_by_comments")
api.add_resource(MostPopular, "//api/most_popular_commenter")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
