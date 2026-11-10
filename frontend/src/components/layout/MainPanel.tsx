import { Box, Toolbar, Typography } from "@mui/material";
import type React from "react"

export interface MainPanelProps {
  children: React.ReactNode;
  title: string;
}


export default (props: MainPanelProps) =>{
  const {children, title} = props;
  return (
    <Box component="main" sx={{ flexGrow: 1, p: 3, maxWidth: "100%", width: "100%", marginLeft: "240px", border: "none"}} >
      <Toolbar />
      <Typography variant="h2" sx={{display: "flex", flexDirection: "row", justifyContent: "space-between"}} >{title}</Typography>
      {children}
    </Box>
  );
}