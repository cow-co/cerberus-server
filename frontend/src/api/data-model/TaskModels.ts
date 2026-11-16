
export type TaskTypeParamResponse = {
  id: string,
  name: string,
  param_type: string,
}

export type TaskTypeResponse = {
  id: string,
  name: string,
  params: TaskTypeParamResponse[]
}

export type TaskTypeParamRequest = {
  name: string,
  param_type: string,
}

export type TaskTypeRequest = {
  name: string,
  params: TaskTypeParamRequest[],
}

export type ArgResponse = {
  id: string,
  spec: TaskTypeParamResponse,
  value: string | number | boolean | null,
}

export type TaskResponse = {
  id: string,
  name: string,
  implant_id: string,
  task_args: ArgResponse[],
}

export type ArgRequest = {
  spec: TaskTypeParamResponse,
  value: string | number | boolean | null,
}

export type TaskRequest = {
  name: string,
  implant_id: string,
  task_args: ArgRequest[],
}