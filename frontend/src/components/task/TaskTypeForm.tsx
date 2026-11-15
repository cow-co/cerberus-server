import {
  Box,
  Button,
  Card,
  FormControl,
  FormLabel,
  InputLabel,
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
  const [params, setParams] = useState<TaskTypeParamRequest[]>([]);

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
    createMutation.mutate({
      name: name,
      params: params,
    });
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
              variant="outlined"
              value={name}
              onChange={(evt) => setName(evt.target.value)}
            />
          </FormControl>
          <Stack direction="column">
            {params.map((param, idx) => {
              return (
                <Stack direction="row">
                  <FormControl fullWidth>
                    <FormLabel>Parameter Name</FormLabel>
                    <TextField
                      id={`param-name-${idx}`}
                      required
                      variant="outlined"
                      value={param.name}
                      onChange={(evt) => updateParamName(idx, evt.target.value)}
                    />
                  </FormControl>
                  <FormControl fullWidth>
                    <InputLabel id={`param-type-select-label-${idx}`}>
                      Type
                    </InputLabel>
                    <Select
                      labelId={`param-type-select-label-${idx}`}
                      id={`param-type-select-${idx}`}
                      value={param.param_type}
                      label="Type"
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
