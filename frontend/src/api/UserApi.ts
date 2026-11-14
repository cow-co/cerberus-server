import { BASE_URL, makeAuthenticatedRequest } from "./ApiUtils";
import type {
  CreateUserRequest,
  LoginRequest,
  LoginResponse,
  NewPasswordRequest,
  UserResponse,
} from "./data-model/UserModels";

export const login = async (
  request: LoginRequest,
): Promise<LoginResponse> => {
  return makeAuthenticatedRequest("POST", "/security/authenticate", request);
};

export const logout = async (): Promise<void> => {
  return makeAuthenticatedRequest("DELETE", "/security/unauthenticate");
};

export const getUsers = async (): Promise<UserResponse[]> => {
  return makeAuthenticatedRequest("GET", "/users");
};


export const createUser = async (payload: CreateUserRequest): Promise<UserResponse> => {
  return makeAuthenticatedRequest("POST", "/users", payload);
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

export const updatePassword = async (payload: NewPasswordRequest): Promise<void> => {
  return makeAuthenticatedRequest("PATCH", "/users/change-password", payload);
}


export const resetPassword = async (userId: string): Promise<string> => {
  return makeAuthenticatedRequest("PATCH", `/users/reset-password/${userId}`);
}