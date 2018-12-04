from flask import (
    Blueprint,
    current_app)
from flask_restful import Api, Resource, reqparse, abort
import flask_login
from flask_sqlalchemy import sqlalchemy

from validator import max_length
# models
from models.Media import Media as MediaModel

blue = Blueprint('media', __name__)
api = Api(blue)

class Media(Resource):
    def get(self, id):
        """Gets a single media."""
        media = MediaModel.query.filter_by(id=int(id)).first()
        return media.name if media else None

    @flask_login.login_required
    def delete(self, id):
        media = MediaModel.query.filter_by(id=int(id)).first()
        db = current_app.config['media.db']
        session = db.session
        try:
            session.delete(media)
            session.commit()
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            # TODO log
            abort(500)
        return 'Success!'

class MediaList(Resource):

    def get(self):
        """Returns all media."""
        medialist = MediaModel.query.all()
        return [ media.name for media in medialist ]

    @flask_login.login_required
    def post(self):
        """Adds new media element to media list."""
        parser = reqparse.RequestParser(trim=True)
        # ---
        parser.add_argument('src',
            type=max_length(1024, str),
            required=True,
            location='form')
        parser.add_argument('name',
            type=max_length(128, str),
            required=True,
            location='form')
        parser.add_argument('license',
            type=max_length(64, str),
            required=True,
            location='form')
        parser.add_argument('description',
            type=max_length(4096, str),
            required=False,
            location='form')
        # TODO: Width and height will be calculated here
        args = parser.parse_args(strict=True)
        # ---
        media = MediaModel(
            src=args.src,
            name=args.name,
            license=args.license,
            description=args.description,
            width=0,
            height=0)
        db = current_app.config['media.db']
        session = db.session
        try:
            session.add(media)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO log error
            abort(500)
        return 'Success!'

api.add_resource(Media, '/<int:id>')
api.add_resource(MediaList, '/')