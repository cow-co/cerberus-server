import type {
  LoginRequest,
  LoginResponse,
  UserResponse,
} from "./data-model/UserModels";

export const login = async (
  request: LoginRequest,
): Promise<LoginResponse> => {
  try {
    const csrfResponse = await fetch("/security/csrf");
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch("/security/authenticate", {
        method: "POST",
        headers: { "X-CSRF-Token": content.token },
        body: JSON.stringify(request),
      });
      if (!response.ok) {
        const content = response.json();
        throw Error(JSON.stringify(content));
      }
      return response.json();
    } else {
      const content = csrfResponse.json();
      throw Error(JSON.stringify(content));
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
};

export const logout = async (): Promise<void> => {
  try {
    const csrfResponse = await fetch("/security/csrf");
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch("/security/unauthenticate", {
        method: "DELETE",
        headers: { "X-CSRF-Token": content.token },
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
    const response = await fetch("/users");
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
