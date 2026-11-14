
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