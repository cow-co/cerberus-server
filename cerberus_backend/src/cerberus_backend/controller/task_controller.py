import uuid
from typing import cast

from cerberus_backend.model.db.task import (
    Task,
    TaskArg,
    TaskParam,
    TaskType,
    create_db_task,
    create_db_task_type,
    get_all_db_task_types,
    get_all_db_tasks,
    get_db_task_by_id,
    get_db_task_type_by_id,
)
from cerberus_backend.model.http.task import (
    TaskArgDTO,
    TaskDTO,
    TaskParamDTO,
    TaskTypeDTO,
)


def create_task_type(task_type: TaskTypeDTO) -> TaskTypeDTO:
    tt = create_db_task_type(
        TaskType(
            name=task_type.name,
            params=[
                TaskParam(
                    name=p.name,
                    param_type=p.param_type,
                )
                for p in task_type.params
            ],
        )
    )
    return TaskTypeDTO(
        id=tt.id,
        name=tt.name,
        params=[TaskParamDTO(
            param_id=p.id,
            name=p.name,
            param_type=p.param_type,
        ) for p in tt.params]
    )


def get_all_task_types() -> list[TaskTypeDTO]:
    response = []
    for tt in get_all_db_task_types():
        print(tt)
        response.append(TaskTypeDTO(
            id=tt.id,
            name=tt.name,
            params=[TaskParamDTO(
                param_id=p.id,
                name=p.name,
                param_type=p.param_type,
            ) for p in tt.params]
        ))
    return response


def get_task_type(tt_id: uuid.UUID) -> TaskType | None:
    tt = get_db_task_type_by_id(tt_id)
    if tt:
        return TaskTypeDTO(
            id=tt.id,
            name=tt.name,
            params=[TaskParamDTO(
                param_id=p.id,
                name=p.name,
                param_type=p.param_type,
            ) for p in tt.params]
        )
    return None


def create_task(task: TaskDTO) -> TaskDTO:
    created = create_db_task(
        Task(
            name=task.name,
            params=[
                TaskArg(
                    spec=TaskParam(
                        id=a.spec.param_id,
                        name=a.spec.name,
                        param_name=a.spec.param_name,
                    )
                )
                for a in task.task_args
            ],
        )
    )
    return TaskDTO(
        task_id=cast(uuid.UUID, created.id),
        name=created.name,
        task_args=[
            TaskArgDTO(
                arg_id=a.arg_id,
                spec=TaskParamDTO(
                    id=a.spec.param_id,
                    name=a.spec.name,
                    param_name=a.spec.param_name,
                ),
                value=a.value,
            )
            for a in created.args
        ],
    )


def get_all_tasks() -> list[TaskDTO]:
    response = []
    for task in get_all_db_tasks():
        response.append(
            TaskDTO(
                task_id=cast(uuid.UUID, task.id),
                name=task.name,
                task_args=[
                    TaskArgDTO(
                        arg_id=a.arg_id,
                        spec=TaskParamDTO(
                            id=a.spec.param_id,
                            name=a.spec.name,
                            param_name=a.spec.param_name,
                        ),
                        value=a.value,
                    )
                    for a in task.args
                ],
            )
        )
    return response


def get_task(task_id: uuid.UUID) -> TaskDTO | None:
    task = get_db_task_by_id(task_id)
    if task:
        return TaskDTO(
            task_id=cast(uuid.UUID, task.id),
            name=task.name,
            task_args=[
                TaskArgDTO(
                    arg_id=a.arg_id,
                    spec=TaskParamDTO(
                        id=a.spec.param_id,
                        name=a.spec.name,
                        param_name=a.spec.param_name,
                    ),
                    value=a.value,
                )
                for a in task.args
            ],
        )
    return None
