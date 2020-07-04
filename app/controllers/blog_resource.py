#pylint: disable=R0201
"""Blog Resource Controller"""
from flask import current_app
from flask_restx import Resource, abort, fields
import flask_login
from flask_sqlalchemy import sqlalchemy
from app.models.blog_resource_entity import BlogResourceEntity
from app.definitions import ROUTING
from app.models.api import API

BLOG_RES_NAMESPACE = API.namespace(
    ROUTING['RI']['BLOG']['namespace'],
    description='Blog resource management',
)

BLOG_DOC = API.model('BlogResource', {
    'resource': fields.String(
        required=True,
        description='Unique resource identifier',
        example='my-blog',
        pattern=BlogResourceEntity.RI_PATTERN,
        **BlogResourceEntity.RI_LENGTH,
    ),
})

@BLOG_RES_NAMESPACE.route(ROUTING['RI']['BLOG']['LIST'])
class BlogResourceList(Resource):
    """Handles blog resources"""

    @API.marshal_with(BLOG_DOC, as_list=True)
    def get(self):
        """Returns all blogs."""
        return BlogResourceEntity.query.all()

    @flask_login.login_required
    @API.doc(security='cookie', body=BLOG_DOC)
    @API.marshal_with(BLOG_DOC, as_list=True)
    def post(self):
        """Adds a new blog resource."""
        new_blog = BlogResourceEntity(**API.payload)
        database = current_app.config['database']
        try:
            database.session.add(new_blog)
            database.session.commit()
        except sqlalchemy.exc.IntegrityError:
            current_app.logger.exception('Post blog integrity error in db')
            return abort(409)
        return [new_blog]
