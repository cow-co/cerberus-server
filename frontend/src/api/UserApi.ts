import type {
  LoginRequest,
  LoginResponse,
  UserResponse,
} from "./data-model/UserModels";

export const login = async (
  request: LoginRequest,
): Promise<LoginResponse | null> => {
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
        console.warn(response.json()); // TODO Throw instead
        return null;
      }
      return response.json();
    } else {
      return null; // TODO Throw instead
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
        console.warn(response.json()); // TODO Throw instead
      }
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
      console.warn(response.json()); // TODO Throw instead
      return [];
    }
  } catch (err) {
    console.warn(err);
    throw err;
  }
};
