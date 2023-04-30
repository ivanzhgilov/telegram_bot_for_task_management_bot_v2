from flask import Flask

import resourses.users_restful
import resourses.tasks_restful
from values import SECRET_KEY, PORT, HOST
from data import db_session
from flask_restful import Api
from flask import make_response, jsonify
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init('db/blogs.sqlite')

    api.add_resource(resourses.tasks_restful.TasksAllListResource, '/api/task/all')
    api.add_resource(resourses.tasks_restful.TasksUserListResource, '/api/task/user/<int:user_id>')
    api.add_resource(resourses.tasks_restful.TaskResource, '/api/task/<int:task_id>')

    api.add_resource(resourses.users_restful.UserResource, '/api/user/<int:user_id>')
    api.add_resource(resourses.users_restful.UsersAllListResource, '/api/user/all')
    api.add_resource(resourses.users_restful.UserIdForTelegramResource, '/api/user/telegram/<int:telegram_id>')

    app.run(port=PORT, host=HOST, debug=True)


if __name__ == '__main__':
    main()
