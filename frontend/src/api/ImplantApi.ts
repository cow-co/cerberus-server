import { makeAuthenticatedRequest } from "./ApiUtils";
import type { ImplantResponse } from "./data-model/ImplantModels";


export const getImplants = async (): Promise<ImplantResponse[]> => {
  return makeAuthenticatedRequest("GET", "/implants");
}