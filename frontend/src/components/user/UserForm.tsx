import { Box, Button, Card, Container, FormControl, FormLabel, TextField } from "@mui/material";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";


export default () => {
  const client = useQueryClient();
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
      setAlertContent(err.message); // TODO redux alert state; alert bar under navbar
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
        passwordConf: passwordConf,
        role: role,
      });
    }
  };

  return (
    <Container>
      <Card>
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
          <FormControl>
            <FormLabel>Password</FormLabel>
            <TextField 
              id="passwordConf" 
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
          <Button fullWidth variant="contained" onClick={submit}>Create</Button>
        </Box>
      </Card>
    </Container>
  );
}