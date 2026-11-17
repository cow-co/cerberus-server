import { makeAuthenticatedRequest } from "./ApiUtils";
import type { TaskRequest, TaskResponse, TaskTypeRequest, TaskTypeResponse } from "./data-model/TaskModels";


export const getTaskTypes = async (): Promise<TaskTypeResponse[]> => {
  return makeAuthenticatedRequest("GET", "/task-types");
}

export const getTaskType = async (ttId: string): Promise<TaskTypeResponse> => {
  return makeAuthenticatedRequest("GET", `/task-types/${ttId}`);
}


export const createTaskType = async (payload: TaskTypeRequest): Promise<TaskTypeResponse> => {
  return makeAuthenticatedRequest("POST", "/task-types", payload);
}


export const createTask = async (payload: TaskRequest): Promise<TaskResponse> => {
  return makeAuthenticatedRequest("POST", "/tasks", payload);
}