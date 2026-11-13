import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "./store";


export interface AuthState {
  username: string | null;
};

const initialState: AuthState = {
  username: localStorage.getItem("username"),
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    updateUsername: (state, action: PayloadAction<string|null>) => {
      state.username = action.payload;
    }
  }
});

export const {updateUsername} = authSlice.actions;
export const selectUsername = (state: RootState) => state.auth.username;
export default authSlice.reducer;