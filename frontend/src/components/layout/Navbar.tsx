import { AppBar, Button, Toolbar, Typography } from "@mui/material";

export default () => {
  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          CERBERUS
        </Typography>
        <Button color="inherit">Implants</Button>
        <Button color="inherit">Task Types</Button>
        <Button color="inherit">Users</Button>
        <Button color="inherit" href="/signin">Login</Button>
      </Toolbar>
    </AppBar>
  );
}