import { AppBar, Button, Toolbar, Typography } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../state/hooks";
import { logout } from "../../api/UserApi";
import { useMutation } from "@tanstack/react-query";
import { updateUsername } from "../../state/authSlice";
import { useNavigate } from "react-router";

export default () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const username = useAppSelector(state => state.auth.username);
  
  const signoutMutation = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      console.log("Signed Out");
      dispatch(updateUsername(null));
      localStorage.removeItem("username");
      navigate("/signin");
    },
  });

  const loginBtn = username ? <Button color="inherit" onClick={() => signoutMutation.mutate()}>Log Out</Button> : <Button color="inherit" href="/signin">Log In</Button>;
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