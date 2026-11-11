import { AppBar, Button, Toolbar, Typography } from "@mui/material";
import { useAppSelector } from "../../state/hooks";

export default () => {
  const username = useAppSelector(state => state.auth.username);
  // TODO execute a logout when logout is clicked
  // TODO On logout, remove username from localstorage
  const loginBtn = username ? <Button color="inherit">Log Out</Button> : <Button color="inherit" href="/signin">Log In</Button>;
  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          CERBERUS
        </Typography>
        <Button color="inherit">Implants</Button>
        <Button color="inherit">Task Types</Button>
        <Button color="inherit" href="/users">Users</Button>
        {loginBtn}
      </Toolbar>
    </AppBar>
  );
}