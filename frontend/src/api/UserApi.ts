import { BASE_URL } from "./ApiUtils";
import { APIResponseError } from "./data-model/Errors";
import type {
  LoginRequest,
  LoginResponse,
  UserResponse,
} from "./data-model/UserModels";

export const login = async (
  request: LoginRequest,
): Promise<LoginResponse> => {
  try {
    const csrfResponse = await fetch(
      `${BASE_URL}/security/csrf`, {
        credentials: "include",});
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch(`${BASE_URL}/security/authenticate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": content.csrf_token,
        },
        credentials: "include",
        body: JSON.stringify(request),
      });
      if (!response.ok) {
        const content = response.json();
        throw new APIResponseError(JSON.stringify(content));
      }
      return response.json();
    } else {
      const content = csrfResponse.json();
      throw new APIResponseError(JSON.stringify(content));
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
};

export const logout = async (): Promise<void> => {
  try {
    const csrfResponse = await fetch(`${BASE_URL}/security/csrf`);
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch(`${BASE_URL}/security/unauthenticate`, {
        method: "DELETE",
        headers: { "X-CSRF-Token": content.csrf_token },
      });
      if (!response.ok) {
        const content = response.json();
        throw Error(JSON.stringify(content));
      }
    } else {
      const content = csrfResponse.json();
      throw Error(JSON.stringify(content));
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
};

export const getUsers = async (): Promise<UserResponse[]> => {
  try {
    const response = await fetch(`${BASE_URL}/users`);
    if (response.ok) {
      return response.json();
    } else {
        const content = response.json();
        throw Error(JSON.stringify(content));
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
};
