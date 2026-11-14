import { Box, Button, FormControl, FormLabel, TextField, Typography, Alert } from "@mui/material";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { login } from "../api/UserApi";
import { useAppDispatch } from "../state/hooks";
import { setNeedsPWChange, updateUsername } from "../state/authSlice";
import type { LoginResponse } from "../api/data-model/UserModels";
import { useNavigate } from "react-router";
import { StandaloneCard, StandaloneContainer } from "../components/layout/StandaloneCards";

export default () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const [username, setUsername] = useState<string>("");
  const [usernameError, setUsernameError] = useState<string|null>(null);
  const [password, setPassword] = useState<string>("");
  const [passwordError, setPasswordError] = useState<string|null>(null);
  const [alertContent, setAlertContent] = useState<string>("");

  const signinMutation = useMutation({
    mutationFn: login,
    onSuccess: (data: LoginResponse) => {
      dispatch(updateUsername(data.username));
      localStorage.setItem("username", data.username);
      dispatch(setNeedsPWChange(data.requires_password_change));
      localStorage.setItem("requiresPWChange", data.requires_password_change ? "true" : "false");
      if (data.requires_password_change) {
        navigate("/change-password");
      } else {
        navigate("/");
      }
    },
    onError: (err) => {
      setAlertContent(err.message);
    },
  });

  const submit = () => {
    if (username.length === 0) {
      setUsernameError("You must enter a username!");
    } else {
      setUsernameError(null);
    }
    if (password.length === 0) {
      setPasswordError("You must enter a password!");
    } else {
      setPasswordError(null);
    }
    if (username.length > 0 && password.length > 0) {
      signinMutation.mutate({
        username: username,
        password: password,
      });
    }
  };

  const alert = alertContent ? <Alert severity="error" variant="filled">{alertContent}</Alert> : <></>;

  return (
    <StandaloneContainer>
      <StandaloneCard variant="outlined">
        <Typography component="h1" variant="h4">Sign In to CERBERUS</Typography>
        {alert}
        <Box 
          sx={{
            display: 'flex',
            flexDirection: 'column',
            width: '100%',
            gap: 2,
          }}
        >
          <FormControl>
            <FormLabel>Username</FormLabel>
            <TextField 
              id="username" 
              fullWidth 
              autoFocus
              required 
              error={usernameError !== null}
              helperText={usernameError}
              color={usernameError ? "error" : "primary"}
              variant="outlined" 
              value={username} 
              onChange={(evt) => setUsername(evt.target.value)}
            />
          </FormControl>
          <FormControl>
            <FormLabel>Password</FormLabel>
            <TextField 
              id="password" 
              fullWidth 
              required 
              error={passwordError !== null}
              helperText={passwordError}
              color={passwordError ? "error" : "primary"}
              type="password" 
              variant="outlined" 
              value={password} 
              onChange={(evt) => setPassword(evt.target.value)}
            />
          </FormControl>
          <Button fullWidth variant="contained" onClick={submit}>Sign In</Button>
        </Box>
      </StandaloneCard>
    </StandaloneContainer>
  );
}