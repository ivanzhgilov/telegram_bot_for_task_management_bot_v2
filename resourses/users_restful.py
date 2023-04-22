from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.users import User
from utils import abort_if_task_not_found, abort_if_user_not_found

update_parser = reqparse.RequestParser()
update_parser.add_argument('name', type=str)
update_parser.add_argument('surname', type=str)
update_parser.add_argument('email', type=str)
update_parser.add_argument('date_of_birth')


class UserResource(Resource):
    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = update_parser.parse_args()
        session = db_session.create_session()
        user: User = session.query(User).where(User.id == user_id)
        for el, key in enumerate(args):
            if el:
                if key == 'name':
                    user.name = el
                elif key == 'surname':
                    user.surname = el
                elif key == 'email':
                    user.email = el
                elif key == 'date_of_birth':
                    user.date_of_birth = el
        session.commit()
        return jsonify({'success': 'OK'})


class UserIdForTelegramResource(Resource):
    def get(self, telegram_id):
        session = db_session.create_session()
        user: User = session.query(User).where(User.telegram_id == telegram_id)
        return jsonify({'user_id': user.id})


add_parser = reqparse.RequestParser()
add_parser.add_argument('telegram_id', required=True)
add_parser.add_argument('name', required=True, type=str)
add_parser.add_argument('surname', required=True, type=str)
add_parser.add_argument('email', required=True, type=str)
add_parser.add_argument('date_of_birth', required=True)


# noinspection PyArgumentList
class UsersAllListResource(Resource):
    def post(self):
        args = add_parser.parse_args()
        session = db_session.create_session()
        user = User(
            **args
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({"users": [item.to_dict(
            only=('name', 'surname', 'created_date')) for item in users]})
