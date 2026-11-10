import { Container, Stack, Typography } from "@mui/material";
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
    <Container sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <Stack sx={{ flex: 1, my: 2 }} spacing={2}>
        <Typography variant="h4">{title}</Typography>
        {children}
      </Stack>
    </Container>
  );
}