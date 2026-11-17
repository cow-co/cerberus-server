// TODO THis should be a modal dialogue

import { useState } from "react"
import { type ArgRequest, type TaskTypeResponse } from "../../api/data-model/TaskModels";
import { Button, FormControl, FormLabel, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createTask, getTaskTypes } from "../../api/TaskApi";
import { useAppDispatch } from "../../state/hooks";
import { setAlertContent } from "../../state/alertSlice";

export interface TaskFormProps {
  implant_id?: string,
}

export default (props: TaskFormProps) => {
  const { implant_id } = props;
  const client = useQueryClient();
  const typesQuery = useQuery({queryKey: ["taskTypes"], queryFn: getTaskTypes});
    const dispatch = useAppDispatch();
  
  const [name, setName] = useState<string>("");
  const [nameError, setNameError] = useState<string|null>(null);
  const [taskType, setTaskType] = useState<TaskTypeResponse|null>(null);
  const [args, setArgs] = useState<ArgRequest[]>([]);

  const createMutation = useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      client.invalidateQueries({queryKey: ["tasks"]});
    },
    onError: (err) => {
      dispatch(setAlertContent({
        alertContent: err.message,
        alertType: "ERROR",
      }));
    },
  });

  const selectTaskType = (id: string) => {
    const found = typesQuery.data?.find(tt => tt.id === id)
    setTaskType(found ? found : null);
    let newArgs: ArgRequest[] = []
    found?.params.forEach(p => newArgs.push({
      spec: p,
      value: null,
    }));
    setArgs(newArgs);
  }

  const submit = () => {
    let valid = true;

    if (name.trim().length === 0) {
      setNameError("You must provide a name!");
      valid = false;
    } else {
      setNameError(null);
    }
    if (implant_id === undefined) {
      valid = false;
    } else {
      if (valid) {
        createMutation.mutate({
          implant_id,
          name,
          task_args: args,
        })
      }
    }
  }

  return (
    <>
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
        <FormControl fullWidth>
          <InputLabel id="type-select-label">Type</InputLabel>
          <Select labelId="type-select-label" id="type-select" value={taskType?.name} label="Type" onChange={(evt) => selectTaskType(evt.target.value)}>
            {typesQuery.data?.map(tt => <MenuItem value={tt.id}>{tt.name}</MenuItem>)}
          </Select>
        </FormControl>
      </FormControl>
      <Button fullWidth variant="contained" onClick={submit}>Create</Button>
    </>
  );
}