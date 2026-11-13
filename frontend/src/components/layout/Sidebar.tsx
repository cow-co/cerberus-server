import { Box, Drawer, Toolbar, Typography } from "@mui/material";
import type React from "react"

export interface SidebarProps {
  children: React.ReactNode;
  title: string;
}

/**
 * The sidebar is meant to display a list of the high-level entities we're looking at
 * (eg. users on the User page), with a short summary of each (eg. just the username)
 * which, when clicked, will open that entity in the main pane.
 */
export default (props: SidebarProps) => {
  const { children, title } = props;

  return (
    <Drawer variant="permanent"sx={{
          width: 240,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
        }}>
      <Toolbar />
      <Box sx={{overflow: "auto"}}>
        <Typography variant="h4" align="center">{title}</Typography>
        {children}
      </Box>
    </Drawer>
  );
}