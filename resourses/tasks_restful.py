from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.tasks import Task
from utils import abort_if_task_not_found, abort_if_user_not_found

update_parser = reqparse.RequestParser()
update_parser.add_argument('is_completed', required=True)
update_parser.add_argument('execution_time', required=True)


class TaskResource(Resource):
    def get(self, task_id):
        abort_if_task_not_found(task_id)
        with db_session.create_session() as session:
            task: Task = session.query(Task).filter(Task.id == task_id).first()
        return jsonify({"task": task.to_dict(
            only=('title', 'content', 'execution_time', 'is_completed', 'user_id', "start_time"))})

    def put(self, task_id):
        abort_if_task_not_found(task_id)
        args = update_parser.parse_args()
        with db_session.create_session() as session:
            task: Task = session.query(Task).filter(Task.id == task_id).first()
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
        with db_session.create_session() as session:
            tasks = session.query(Task).all()
        return jsonify({'tasks': [item.to_dict(
            only=('title', 'content', 'id', 'user_id', 'is_completed')) for item in tasks]})

    def post(self):
        args = add_parser.parse_args()
        with db_session.create_session() as session:
            task = Task(
                **args
            )
            session.add(task)
            session.commit()
        return jsonify({'success': 'OK'})


class TasksUserListResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        with db_session.create_session() as session:
            tasks_all = session.query(Task).all()
            completed_tasks = session.query(Task).filter(Task.is_completed == 1).all()
            not_completed_tasks = session.query(Task).filter(Task.is_completed == 0).all()



            return jsonify({'tasks': [item.to_dict(
                only=('title', 'content', 'execution_time', 'is_completed', 'start_time', 'id'))
                for item in tasks_all], 'completed_tasks': [item.to_dict(
                only=('title', 'content', 'execution_time', 'is_completed', 'start_time', 'id'))
                for item in completed_tasks], 'not_completed_tasks': [item.to_dict(
                only=('title', 'content', 'execution_time', 'is_completed', 'start_time', 'id'))
                for item in not_completed_tasks]})
