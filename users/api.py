import http.client
from flask_restplus import Namespace, Resource, fields
from users.models import UserModel
from users.db import db
from users import config
from users.token_validation import validate_token_header
from users.token_validation import generate_token_header
from flask import abort

api_ns = Namespace('api', description='User API')

model = {
    'id': fields.Integer(),
    'fname': fields.String(),
    'lname': fields.String(),
    'username': fields.String(),
    'email': fields.String()
}

user_model = api_ns.model('User', model)

user_parser = api_ns.parser()
user_parser.add_argument('fname', type=str, help='First Name')
user_parser.add_argument('lname', type=str, help='Last Name')
user_parser.add_argument('username', type=str, help='Username')
user_parser.add_argument('email', type=str, help='Email', required=True)
user_parser.add_argument('password', type=str, help='Password')

authentication_parser = api_ns.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str, help='Bearer Access Token')

login_parser = api_ns.parser()
login_parser.add_argument('email', type=str, required=True, help='email')
login_parser.add_argument('password', type=str, required=True, help='password')


def authentication_header_parser(value):
    email = validate_token_header(value, config.PUBLIC_KEY)
    if email is None:
        abort(401)
    return email


@api_ns.route('/register')
class UserCreate(Resource):
    @api_ns.expect(user_parser)
    @api_ns.marshal_with(user_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new user
        '''
        args = user_parser.parse_args()

        if UserModel.find_by_email(args['email']):
            return {"message": "Email is already registered."}, 400

        new_user = UserModel(
            fname=args['fname'],
            lname=args['lname'],
            username=args['username'],
            email=args['email'])

        new_user.set_password(args['password'])
        new_user.save_to_db()

        result = api_ns.marshal(new_user, user_model)

        return result, http.client.CREATED


@api_ns.route('/login')
class UserLogin(Resource):
    @api_ns.doc('login')
    @api_ns.expect(login_parser)
    def post(self):
        '''
        Login and return a valid Authorization header
        '''
        args = login_parser.parse_args()

        user = UserModel.find_by_email(args['email'])

        if user and user.check_password(args['password']):
            # Generate the header
            header = generate_token_header(user.username, config.PRIVATE_KEY)
            return {'Authorized': header}, http.client.OK

        return {"message": "Invalid email or password"}, http.client.UNAUTHORIZED
