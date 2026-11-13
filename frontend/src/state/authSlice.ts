import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "./store";


export interface AuthState {
  username: string | null;
  requiresPWChange: boolean;
};

const initialState: AuthState = {
  username: localStorage.getItem("username"),
  requiresPWChange: false,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    updateUsername: (state, action: PayloadAction<string|null>) => {
      state.username = action.payload;
    },
    setNeedsPWChange: (state, action: PayloadAction<boolean>) => {
      state.requiresPWChange = action.payload;
    }
  }
});

export const {updateUsername, setNeedsPWChange} = authSlice.actions;
export const selectUsername = (state: RootState) => state.auth.username;
export const needsPWChange = (state: RootState) => state.auth.requiresPWChange;
export default authSlice.reducer;