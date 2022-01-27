
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)
  
   
    def __repr__(self):
        return f"Video(name = {VideoModel.name}, views = {VideoModel.views}, likes = {VideoModel.likes})"  


  
video_put_args = reqparse.RequestParser() #An instanciation
video_put_args.add_argument("name", type=str, help="Name of video is required", required = True)
video_put_args.add_argument("views", type=int, help="Views of video", required = True)
video_put_args.add_argument("likes", type=int, help="Likes of video", required = True)

video_patch_args = reqparse.RequestParser() 
video_patch_args.add_argument("name", type=str, help="Name of video is required")
video_patch_args.add_argument("views", type=int, help="Views of video")
video_patch_args.add_argument("likes", type=int, help="Likes of video")
  
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    "likes": fields.Integer
}

# def empty_dict_error(video_id):
#     if video_id not in videos:
#         abort(404, message = "The list you are trying to access is empty")

# def id_already_exist_error(video_id):
#     if video_id in videos:
#         abort(409, message = "The id of the entry already exists")


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Could not find video with that id")
        return result 

    @marshal_with(resource_fields)
    def put(self, video_id): 
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if result: #if result exits(returs true)
            abort(409, message = "Video id is already taken")
        video = VideoModel(id = video_id, name = args["name"], views = args["views"], likes = args["likes"])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_patch_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Video to update does not exist")
        if args ["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.commit()

        return result



    # def delete(self, video_id):
    #     empty_dict_error(video_id)
    #     del videos[video_id]
    #     return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug = True, port = 5005) 