from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.tasks import Task
from utils import abort_if_task_not_found, abort_if_user_not_found

update_parser = reqparse.RequestParser()
update_parser.add_argument('is_completed', required=True)
update_parser.add_argument('execution_time', default='не засечено')


class TaskResource(Resource):
    def get(self, task_id):
        abort_if_task_not_found(task_id)
        session = db_session.create_session()
        task: Task = session.query(Task).where(Task.id == task_id)
        return jsonify({"task": task.to_dict(
            only=('title', 'content', 'execution_time', 'is_completed', 'user_id', "start_time"))})

    def post(self, task_id):
        abort_if_task_not_found(task_id)
        args = update_parser.parse_args()
        session = db_session.create_session()
        task: Task = session.query(Task).where(Task.id == task_id)
        task.is_completed = args['is_completed']
        task.execution_time = args['execution_time']
        session.commit()
        return jsonify({'success': 'OK'})


add_parser = reqparse.RequestParser()
add_parser.add_argument('title', required=True)
add_parser.add_argument('content', required=True)
add_parser.add_argument('start_time', required=False)
add_parser.add_argument('user_id', required=True)


# noinspection PyArgumentList
class TasksAllListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tasks = session.query(Task).all()
        return jsonify({'tasks': [item.to_dict(
            only=('title', 'content', 'user_id', 'is_completed')) for item in tasks]})

    def post(self):
        args = add_parser.parse_args()
        session = db_session.create_session()
        task = Task(
            **args
        )
        session.add(task)
        session.commit()
        return jsonify({'success': 'OK'})


class TasksUserListResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        tasks = session.query(Task).where(Task.user_id == user_id)
        return jsonify({'tasks': [item.to_dict(
            only=('title', 'content', 'user_id', 'is_completed', 'is_completed', 'start_time')) for item in tasks]})
