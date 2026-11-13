import { updateUsername } from "../state/authSlice";
import { store } from "../state/store";
import { APIResponseError, UnauthenticatedError } from "./data-model/Errors";


export const BASE_URL = "http://localhost/api";   // TODO ENV VAR this

export const makeAuthenticatedRequest = async (method: string, path: string, payload?: Object) => {
  try {
    const csrfResponse = await fetch(`${BASE_URL}/security/csrf`);
    if (csrfResponse.ok) {
      const content = await csrfResponse.json();
      const response = await fetch(`${BASE_URL}${path}`, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": content.csrf_token,
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        console.error("Fetch error");
        if (response.status === 401) {
          store.dispatch(updateUsername(null));
          localStorage.removeItem("username");
          throw new UnauthenticatedError("Not authenticated");
        } else {
          const content = await response.json();
          throw new APIResponseError(content.message);
        }
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