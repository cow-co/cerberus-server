import { Box, Button, Card as MuiCard, FormControl, FormLabel, TextField, Typography, Stack, Alert } from "@mui/material";
import { useState } from "react";
import { styled } from '@mui/material/styles';
import { useMutation } from "@tanstack/react-query";
import { login } from "../api/UserApi";
import { useAppDispatch } from "../state/hooks";
import { updateUsername } from "../state/authSlice";
import type { LoginResponse } from "../api/data-model/UserModels";
import { useNavigate } from "react-router";


const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  margin: 'auto',
  [theme.breakpoints.up('sm')]: {
    maxWidth: '450px',
  },
  boxShadow:
    'hsla(220, 30%, 5%, 0.05) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.05) 0px 15px 35px -5px',
  ...theme.applyStyles('dark', {
    boxShadow:
      'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
  }),
}));

const SignInContainer = styled(Stack)(({ theme }) => ({
  height: 'calc((1 - var(--template-frame-height, 0)) * 100dvh)',
  minHeight: '100%',
  padding: theme.spacing(2),
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(4),
  },
}));

export default () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [alertContent, setAlertContent] = useState<string>("");
  const signinMutation = useMutation({
    mutationFn: login,
    onSuccess: (data: LoginResponse) => {
      dispatch(updateUsername(data.username));
      localStorage.setItem("username", data.username);
      navigate("/");
    },
    onError: (err) => {
      setAlertContent(err.message);
    },
  });

  const submit = () => {
    signinMutation.mutate({
      username: username,
      password: password,
    })
  };

  const alert = alertContent ? <Alert>{alertContent}</Alert> : <></>;

  return (
    <SignInContainer>
      <Card variant="outlined">
        <Typography component="h1" variant="h4">Sign In to CERBERUS</Typography>
        {alert}
        <Box component="form" onSubmit={submit} noValidate sx={{
          display: 'flex',
          flexDirection: 'column',
          width: '100%',
          gap: 2,
        }}>
          <FormControl>
            <FormLabel>Username</FormLabel>
            <TextField id="username" fullWidth autoFocus variant="outlined" value={username} onChange={(evt) => setUsername(evt.target.value)}/>
          </FormControl>
          <FormControl>
            <FormLabel>Password</FormLabel>
            <TextField id="password" fullWidth autoFocus type="password" variant="outlined" value={password} onChange={(evt) => setPassword(evt.target.value)}/>
          </FormControl>
          <Button fullWidth variant="contained" type="submit">Sign In</Button>
        </Box>
      </Card>
    </SignInContainer>
  );
}