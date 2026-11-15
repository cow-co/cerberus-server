import {
  Box,
  Button,
  Card,
  FormControl,
  FormLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
} from "@mui/material";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { setAlertContent } from "../../state/alertSlice";
import { useAppDispatch } from "../../state/hooks";
import { createTaskType } from "../../api/TaskApi";
import type { TaskTypeParamRequest } from "../../api/data-model/TaskModels";

export default () => {
  const client = useQueryClient();
  const dispatch = useAppDispatch();
  const paramTypes = ["INTEGER", "STRING", "BOOLEAN"];

  const [name, setName] = useState<string>("");
  const [nameError, setNameError] = useState<string|null>(null);
  const [params, setParams] = useState<TaskTypeParamRequest[]>([]);
  const [paramErrors, setParamErrors] = useState<string[]>([]);

  const createMutation = useMutation({
    mutationFn: createTaskType,
    onSuccess: () => {
      client.invalidateQueries({ queryKey: ["taskTypes"] });
    },
    onError: (err) => {
      dispatch(
        setAlertContent({
          alertContent: err.message,
          alertType: "ERROR",
        }),
      );
    },
  });

  const submit = () => {
    let valid: boolean = true;
    if (name.trim().length === 0) {
      setNameError("Name cannot be empty!");
      valid = false;
    }

    let newParamErrors: string[] = [];
    params.forEach((param, idx) => {
      if (param.name.trim().length === 0) {
        newParamErrors[idx] = "Name cannot be empty!";
        valid = false;
      } else {
        newParamErrors[idx] = "";
      }
    });
    setParamErrors(newParamErrors);

    if (valid) {
      createMutation.mutate({
        name: name,
        params: params,
      });
    }
  };

  const updateParamName = (idx: number, newName: string) => {
    let newParams = [...params];
    newParams[idx].name = newName;
    setParams(newParams);
  }

  const updateParamType = (idx: number, newType: string) => {
    let newParams = [...params];
    newParams[idx].param_type = newType;
    setParams(newParams);
  }

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Card
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "60%",
        }}
      >
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            width: "100%",
            gap: 2,
            p: "20px",
          }}
        >
          <FormControl fullWidth>
            <FormLabel>Name</FormLabel>
            <TextField
              id="name"
              autoFocus
              required
              error={nameError !== null}
              helperText={nameError ? nameError : ""}
              color={nameError ? "error" : "primary"}
              variant="outlined"
              value={name}
              onChange={(evt) => setName(evt.target.value)}
            />
          </FormControl>
          <Stack direction="column">
            {params.map((param, idx) => {
              return (
                <Stack direction="row" spacing={2}>
                  <FormControl fullWidth>
                    <FormLabel>Parameter Name</FormLabel>
                    <TextField
                      id={`param-name-${idx}`}
                      required
                      error={paramErrors[idx] !== ""}
                      helperText={paramErrors[idx] ? paramErrors[idx] : ""}
                      color={paramErrors[idx] === "" ? "error" : "primary"}
                      variant="outlined"
                      value={param.name}
                      onChange={(evt) => updateParamName(idx, evt.target.value)}
                    />
                  </FormControl>
                  <FormControl fullWidth>
                    <FormLabel>Parameter Type</FormLabel>
                    <Select
                      id={`param-type-select-${idx}`}
                      value={param.param_type}
                      onChange={(evt) => updateParamType(idx, evt.target.value)}
                    >
                      {paramTypes.map((pt) => (
                        <MenuItem value={pt}>{pt}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Stack>
              );
            })}
            <Button onClick={() => setParams([...params, {name: "", param_type: "STRING"}])}>Add Parameter</Button>
          </Stack>
          <Button fullWidth variant="contained" onClick={submit}>
            Create
          </Button>
        </Box>
      </Card>
    </Box>
  );
};
