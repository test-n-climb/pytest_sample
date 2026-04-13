from http import HTTPStatus

from flask import Flask, g, request
from pydantic import ValidationError

from mock_service.db.task_db_client import TaskDbClient
from mock_service.resolvers.create_task_resolver import CreateTaskResolver
from mock_service.resolvers.get_task_resolver import GetTaskResolver
from mock_service.schemas.response import ResponseContent
from mock_service.schemas.task import PostTaskInput

"""Mock Task API service for demonstration purposes."""

app = Flask(__name__)
task_db_client = TaskDbClient()


@app.errorhandler(Exception)
def handle_exception(e):
    return (
        ResponseContent(success=False, errors="Internal Server Error").model_dump_json(),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def get_db():
    if "db" not in g:
        g.db = TaskDbClient()
    return g.db


@app.teardown_appcontext
def shutdown_session(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.remove()


@app.route("/task/create", methods=["POST"])
def create_task():
    try:
        task_input = PostTaskInput(**request.get_json())
    except ValidationError as e:
        return ResponseContent(success=False, errors=str(e.errors())).model_dump_json(), HTTPStatus.UNPROCESSABLE_ENTITY

    created_task = CreateTaskResolver(task_input, get_db()).resolve()

    return ResponseContent(success=True, data=created_task.model_dump_json()).model_dump_json(), HTTPStatus.CREATED


@app.route("/task/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    task = GetTaskResolver(task_id, get_db()).resolve()

    if task is None:
        return ResponseContent(success=False, errors="Task not found").model_dump_json(), HTTPStatus.NOT_FOUND

    return ResponseContent(success=True, data=task.model_dump_json()).model_dump_json(), HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
