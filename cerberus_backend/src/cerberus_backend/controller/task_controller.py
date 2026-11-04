import uuid
from typing import cast

from cerberus_backend.model.common.enums import ParamType
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
    print(task_type)
    tt = create_db_task_type(task_type)
    return TaskTypeDTO(
        id=tt.id,
        name=task_type.name,
        params=task_type.params,    # TODO need to grab the param ids from the created params
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


def get_task_type(tt_id: uuid.UUID) -> TaskTypeDTO | None:
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
            args=[
                TaskArg(
                    param_id=a.spec.param_id,
                    value_str=cast(str, a.value) if a.spec.param_type == ParamType.STRING else None,
                    value_int=cast(int, a.value) if a.spec.param_type == ParamType.INTEGER else None,
                    value_bool=cast(bool, a.value) if a.spec.param_type == ParamType.BOOLEAN else None,
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
                arg_id=a.id,
                spec=TaskParamDTO(
                    param_id=a.spec.id,
                    name=a.spec.name,
                    param_type=a.spec.param_type,
                ),
                value=a.value_str if a.value_str else (a.value_int if a.value_int else a.value_bool),
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
                        arg_id=a.id,
                        spec=TaskParamDTO(
                            param_id=a.spec.id,
                            name=a.spec.name,
                            param_type=a.spec.param_type,
                        ),
                        value=a.value_str if a.value_str else (a.value_int if a.value_int else a.value_bool),
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
