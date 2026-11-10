import { AppBar, Button, Toolbar, Typography } from "@mui/material";

export default () => {
  return (
    <AppBar>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          CERBERUS
        </Typography>
        <Button color="inherit">Implants</Button>
        <Button color="inherit">Task Types</Button>
        <Button color="inherit">Users</Button>
        <Button color="inherit">Login</Button>
      </Toolbar>
    </AppBar>
  );
}