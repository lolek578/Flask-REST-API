from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

videos = {}


def abort_if_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid...")


def abort_if_exist(video_id):
    if video_id in videos:
        abort(409, message="Video is already exists...")


class Video(Resource):
    @staticmethod
    def get(video_id):
        abort_if_doesnt_exist(video_id)
        return videos[video_id]

    @staticmethod
    def put(video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    @staticmethod
    def delete(video_id):
        abort_if_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
    app.run(debug=True)
