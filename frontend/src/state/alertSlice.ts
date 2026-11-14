import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "./store";

export type AlertContent = {
  alertContent: string | null;
  alertType: null | "SUCCESS" | "WARNING" | "ERROR";
}


export interface AlertState {
  alert: AlertContent | null;
};

const initialState: AlertState = {
  alert: {
    alertContent: null,
    alertType: null,
  },
};

export const alertSlice = createSlice({
  name: "alert",
  initialState,
  reducers: {
    setAlertContent: (state, action: PayloadAction<AlertContent|null>) => {
      state.alert = action.payload;
    },
  }
});

export const {setAlertContent} = alertSlice.actions;
export const selectAlert = (state: RootState) => state.alert.alert;
export default alertSlice.reducer;