import { makeAuthenticatedRequest } from "./ApiUtils";
import type { TaskTypeRequest, TaskTypeResponse } from "./data-model/TaskModels";


export const getTaskTypes = async (): Promise<TaskTypeResponse[]> => {
  return makeAuthenticatedRequest("GET", "/task-types");
}


export const createTaskType = async (payload: TaskTypeRequest): Promise<TaskTypeResponse> => {
  return makeAuthenticatedRequest("POST", "/task-types", payload);
}