import { makeAuthenticatedRequest } from "./ApiUtils";
import type { ImplantResponse } from "./data-model/ImplantModels";
import type { TaskResponse } from "./data-model/TaskModels";


export const getImplants = async (): Promise<ImplantResponse[]> => {
  return makeAuthenticatedRequest("GET", "/implants");
}

export const getImplantTasks = async (implantId: string): Promise<TaskResponse[]> => {
  return makeAuthenticatedRequest("GET", `/implants/${implantId}/tasks`);
}