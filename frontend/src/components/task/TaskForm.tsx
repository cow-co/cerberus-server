// TODO THis should be a modal dialogue

import { useState } from "react"
import { type ArgRequest, type TaskTypeResponse } from "../../api/data-model/TaskModels";
import { Button, FormControl, FormLabel, InputLabel, MenuItem, Select, TextField } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { getTaskTypes } from "../../api/TaskApi";


export default () => {
  const typesQuery = useQuery({queryKey: ["taskTypes"], queryFn: getTaskTypes});
  const [name, setName] = useState<string>("");
  const [nameError, setNameError] = useState<string|null>(null);
  const [taskType, setTaskType] = useState<TaskTypeResponse|null>(null);
  const [args, setArgs] = useState<ArgRequest[]>([]);

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