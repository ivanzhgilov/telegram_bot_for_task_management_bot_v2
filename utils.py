from data.tasks import Task
from data.users import User
from data import db_session
from flask_restful import abort


def abort_if_task_not_found(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        abort(404, message=f"Task {task_id} not found")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
