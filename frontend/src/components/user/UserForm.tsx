import { Box, Button, Card, FormControl, FormLabel, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createUser, getRoles } from "../../api/UserApi";
import { setAlertContent } from "../../state/alertSlice";
import { useAppDispatch } from "../../state/hooks";


export default () => {
  const client = useQueryClient();
  const dispatch = useAppDispatch();

  const rolesQuery = useQuery({queryKey: ["roles"], queryFn: getRoles});
  const [username, setUsername] = useState<string>("");
  const [usernameError, setUsernameError] = useState<string|null>(null);
  const [password, setPassword] = useState<string>("");
  const [passwordError, setPasswordError] = useState<string|null>(null);
  const [passwordConf, setPasswordConf] = useState<string>("");
  const [passwordConfError, setPasswordConfError] = useState<string|null>(null);
  const [role, setRole] = useState<string>("");

  
  const createMutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      client.invalidateQueries({queryKey: ["users"]});
    },
    onError: (err) => {
      dispatch(setAlertContent({
        alertContent: err.message,
        alertType: "ERROR",
      }));
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
    if (passwordConf !== password) {
      setPasswordConfError("Password confirmation does not match!");
    } else {
      setPasswordConfError(null);
    }
    if (username.length > 0 && password.length > 0) {
      createMutation.mutate({
        username: username,
        password: password,
        password_confirmation: passwordConf,
        role: role,
      });
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Card
        sx={{
          display: 'flex',
          justifyContent: "center",
          alignItems: "center",
          width: "60%",
        }}
      >
        <Box 
          sx={{
            display: 'flex',
            flexDirection: 'column',
            width: '100%',
            gap: 2,
            p: "20px",
          }}
        >
          <FormControl fullWidth>
            <FormLabel>Username</FormLabel>
            <TextField 
              id="username" 
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
          <FormControl fullWidth>
            <FormLabel>Password</FormLabel>
            <TextField 
              id="password" 
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
          <FormControl fullWidth>
            <FormLabel>Password Confirmation</FormLabel>
            <TextField 
              id="passwordConf"
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
          <FormControl fullWidth>
            <InputLabel id="role-select-label">Role</InputLabel>
            <Select labelId="role-select-label" id="role-select" value={role} label="Role" onChange={(evt) => setRole(evt.target.value)}>
              {rolesQuery.data?.map(role => <MenuItem value={role}>{role}</MenuItem>)}
            </Select>
          </FormControl>
          <Button fullWidth variant="contained" onClick={submit}>Create</Button>
        </Box>
      </Card>
    </Box>
  );
}