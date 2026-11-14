import { Alert, Box, Toolbar, Typography } from "@mui/material";
import type React from "react"
import { useAppSelector } from "../../state/hooks";

export interface MainPanelProps {
  children: React.ReactNode;
  title: string;
}


export default (props: MainPanelProps) =>{
  const {children, title} = props;
  const alertDetails = useAppSelector((state) => state.alert.alert);
  let sev: "success" | "warning" | "error" = "success";
  if (alertDetails?.alertType === "WARNING") {
    sev = "warning";
  } else if (alertDetails?.alertType === "ERROR") {
    sev = "error";
  }
  const alert = alertDetails === null ? <></> : <Alert variant="filled" severity={sev}>{alertDetails.alertContent}</Alert>;
  return (
    <Box component="main" sx={{ flexGrow: 1, p: 3, maxWidth: "100%", marginLeft: "240px", border: "none"}} >
      <Toolbar />
      {alert}
      <Typography variant="h2" sx={{display: "flex", flexDirection: "row", justifyContent: "space-between"}} >{title}</Typography>
      {children}
    </Box>
  );
}