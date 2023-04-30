from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.users import User
from utils import abort_if_task_not_found, abort_if_user_not_found

update_parser = reqparse.RequestParser()
update_parser.add_argument('name', type=str)
update_parser.add_argument('surname', type=str)
update_parser.add_argument('email', type=str)


class UserResource(Resource):
    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = update_parser.parse_args()
        with db_session.create_session() as session:
            user: User = session.query(User).filter(User.id == user_id)
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
        with db_session.create_session() as session:
            user: User = session.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            return jsonify({'user_id': 'not fount'})
        return jsonify({'user_id': user.id})


add_parser = reqparse.RequestParser()
add_parser.add_argument('telegram_id')
add_parser.add_argument('name')
add_parser.add_argument('surname')
add_parser.add_argument('email')


# noinspection PyArgumentList
class UsersAllListResource(Resource):
    def post(self):
        args = add_parser.parse_args()
        with db_session.create_session() as session:
            user = User(
                **args
            )
            session.add(user)
            session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        with db_session.create_session() as session:
            users = session.query(User).all()
            return jsonify({"users": [item.to_dict(
                only=('name', 'surname', 'created_date')) for item in users]})
