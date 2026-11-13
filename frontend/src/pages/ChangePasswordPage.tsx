import { Box, Button, Card as MuiCard, FormControl, FormLabel, TextField, Typography, Stack, Alert } from "@mui/material";
import { useState } from "react";
import { styled } from '@mui/material/styles';
import { useMutation } from "@tanstack/react-query";
import { login, updatePassword } from "../api/UserApi";
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

  const [password, setPassword] = useState<string>("");
  const [passwordError, setPasswordError] = useState<string|null>(null);
  const [newPassword, setNewPassword] = useState<string>("");
  const [newPasswordError, setNewPasswordError] = useState<string|null>(null);
  const [passwordConf, setPasswordConf] = useState<string>("");
  const [passwordConfError, setPasswordConfError] = useState<string|null>(null);
  const [alertContent, setAlertContent] = useState<string>("");

  const pwChangeMutation = useMutation({
    mutationFn: updatePassword,
    onSuccess: () => {
      dispatch(updateUsername(null));
      localStorage.removeItem("username");
      navigate("/signin");
    },
    onError: (err) => {
      setAlertContent(err.message);
    },
  });

  const submit = () => {
    let isValid = true;
    if (password.length === 0) {
      setPasswordError("You must enter your current password!");
      isValid = false;
    } else {
      setPasswordError(null);
    }
    if (newPassword.length === 0) {
      setNewPasswordError("You must enter a new password!");
      isValid = false;
    } else {
      setNewPasswordError(null);
    }
    if (passwordConf !== newPassword) {
      setPasswordConfError("Password confirmation does not match!");
      isValid = false;
    } else {
      setPasswordConfError(null);
    }
    if (isValid) {
      pwChangeMutation.mutate({
        old_password: password,
        password: newPassword,
        password_confirmation: passwordConf,
      });
    }
  };

  const alert = alertContent ? <Alert severity="error" variant="filled">{alertContent}</Alert> : <></>;

  return (
    <SignInContainer>
      <Card variant="outlined">
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
            <FormLabel>Current Password</FormLabel>
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
          <FormControl>
            <FormLabel>New Password</FormLabel>
            <TextField 
              id="password" 
              fullWidth 
              required 
              error={newPasswordError !== null}
              helperText={newPasswordError}
              color={newPasswordError ? "error" : "primary"}
              type="password" 
              variant="outlined" 
              value={newPassword} 
              onChange={(evt) => setNewPassword(evt.target.value)}
            />
          </FormControl>
          <FormControl>
            <FormLabel>Password Confirmation</FormLabel>
            <TextField 
              id="password" 
              fullWidth 
              required 
              error={passwordConfError !== null}
              helperText={passwordConfError}
              color={passwordConfError ? "error" : "primary"}
              type="password" 
              variant="outlined" 
              value={passwordConf} 
              onChange={(evt) => setPasswordConf(evt.target.value)}
            />
          </FormControl>
          <Button fullWidth variant="contained" onClick={submit}>Change Password</Button>
        </Box>
      </Card>
    </SignInContainer>
  );
}