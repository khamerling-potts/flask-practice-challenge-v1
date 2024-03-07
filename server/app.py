from config import app, api
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func


# create routes here:
class SortedPosts(Resource):
    def get(self):
        posts = [post.to_dict() for post in Post.query.order_by("title")]
        # posts.sort(key=lambda post: post.get("title"))
        return posts, 200


class PostsByAuthor(Resource):
    def get(self, author_name):
        posts = [
            post.to_dict() for post in Post.query.filter_by(author=author_name.title())
        ]
        return posts, 200


class SearchPosts(Resource):
    def get(self, title):
        posts = [
            post.to_dict() for post in Post.query.filter(Post.title.contains(title))
        ]
        # Should I be doing the filtering after the query?
        # I couldn't figure out how to add case insensitivity to Post.title within the query itself.
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
            commenter = comment.commenter
            if commenter in counts:
                counts[commenter] += 1
            else:
                counts[commenter] = 1
        max_commenter = max(counts, key=lambda person: counts[person])
        return {"commenter": max_commenter}, 200


# My own challenge: Finds any posts where the given commenter commented on it
class PostsWithCommenter(Resource):
    def get(self, commenter):
        result = []
        posts = [post.to_dict() for post in Post.query.all()]
        for post in posts:
            commenters = [comment["commenter"] for comment in post["comments"]]
            if commenters.count(commenter.title()):
                result.append(post)

        return result, 200


api.add_resource(SortedPosts, "/api/sorted_posts")
api.add_resource(PostsByAuthor, "/api/posts_by_author/<author_name>")
api.add_resource(SearchPosts, "/api/search_posts/<title>")
api.add_resource(PostsByComments, "/api/posts_ordered_by_comments")
api.add_resource(MostPopular, "/api/most_popular_commenter")
api.add_resource(PostsWithCommenter, "/api/posts_with_commenter/<commenter>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
