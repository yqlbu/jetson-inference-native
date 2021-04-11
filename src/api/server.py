from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


prin("nihaoma")k


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


# only initialize DB once
#  db.create_all()

# PUT
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="Likes of the video is required", required=True)

# PATCH
video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    # when we return, take that return value and serialized with the resource_fields in JSON format

    # GET
    @marshal_with(resource_fields)  # decorator
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, msg='Could not find video with that id...')
        return result, 200

    # POST
    @marshal_with(resource_fields)  # decorator
    def put(self, video_id):
        args = video_put_args.parse_args()
        # prevent dulplicate id
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, msg='Video id is taken...')
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201  # 201 stands for created

    # UPDATE
    @marshal_with(resource_fields)  # decorator
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, msg='Video does not exist, cannot update...')

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result, 200

#  def delete(self, video_id):
#      del videos[video_id]
#      return '', 201


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
