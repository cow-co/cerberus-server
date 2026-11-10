import type { LoginRequest } from "./data-model/UserModels";


export const login = async (request: LoginRequest) => {
  try {
    // TODO actual API url
    const response = await fetch("")
  } catch (err) {
    // TODO Do something better with it
    console.warn(err);
  }
};