import { BASE_URL } from "./ApiUtils";
import { APIResponseError } from "./data-model/Errors";
import type {
  CreateUserRequest,
  LoginRequest,
  LoginResponse,
  UserResponse,
} from "./data-model/UserModels";

export const login = async (
  request: LoginRequest,
): Promise<LoginResponse> => {
  try {
    const csrfResponse = await fetch(`${BASE_URL}/security/csrf`);
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch(`${BASE_URL}/security/authenticate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": content.csrf_token,
        },
        body: JSON.stringify(request),
      });
      if (!response.ok) {
        const content = await response.json();
        console.error("Fetch error");
        throw new APIResponseError(content.message);
      }
      return response.json();
    } else {
      const content = await csrfResponse.json();
      console.error("CSRF token error");
      throw new APIResponseError(content.message);
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
        const content = await response.json();
        console.error("Fetch error");
        throw Error(content.message);
      }
    } else {
      const content = await csrfResponse.json();
      console.error("CSRF token error");
      throw Error(content.message);
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
        const content = await response.json();
        console.error("Fetch error");
        throw Error(content.message);
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
};


export const createUser = async (payload: CreateUserRequest): Promise<UserResponse> => {
  try {
    const csrfResponse = await fetch(
      `${BASE_URL}/security/csrf`, {
        credentials: "include",});
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch(`${BASE_URL}/users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": content.csrf_token,
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const content = await response.json();
        console.error("Fetch error");
        throw new APIResponseError(content.message);
      }
      return response.json();
    } else {
      const content = await csrfResponse.json();
      console.error("CSRF token error");
      throw new APIResponseError(content.message);
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
}


export const getRoles = async (): Promise<string[]> => {
  try {
    const response = await fetch(`${BASE_URL}/users/roles`);
    if (response.ok) {
      return response.json();
    } else {
        const content = await response.json();
        console.error("Fetch error");
        throw Error(content.message);
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
}
