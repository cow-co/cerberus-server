import BasePageLayout from "../components/layout/BasePageLayout";
import { useQuery } from "@tanstack/react-query";
import { List, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import type { TaskTypeResponse } from "../api/data-model/TaskModels";
import { getTaskType, getTaskTypes } from "../api/TaskApi";
import TaskTypeShow from "../components/task/TaskTypeShow";
import TaskTypeForm from "../components/task/TaskTypeForm";
import { useLocation } from "react-router";
import { isUUID } from "../utils";


const generateTTQuery = (ttId: string | null) => {
  return useQuery({
    queryFn: (): Promise<TaskTypeResponse> => {
      if (ttId) {
        return getTaskType(ttId);
      } else {
        return Promise.reject("No tasktype ID provided");
      }
    },
    queryKey: ["taskType", ttId],
  })
}

export default () => {
  const loc = useLocation();
  const path_elements = loc.pathname.split("/");
  const maybeId = path_elements.at(-1);
  if (!maybeId) {
    return <></>;
  }
  let ttId: string|null = isUUID(maybeId) ? maybeId : null;
  const taskTypesQuery = useQuery({queryKey: ["taskTypes"], queryFn: getTaskTypes});
  const taskTypeQuery = generateTTQuery(ttId);

  const sidebarContent = taskTypesQuery.isSuccess ? (
    <List>
      {taskTypesQuery.data!.map(tt => {
        return (
        <ListItemButton href={`/task-types/view/${tt.id}`}>
          <ListItemText>{tt.name}</ListItemText>
        </ListItemButton>
        );
      })}
      <ListItemButton href="/task-types">
        <ListItemIcon><AddIcon /></ListItemIcon>
        <ListItemText>Create</ListItemText>
      </ListItemButton>
    </List>
  ) : <></>;
  const sidebarProps = {
    title: "Task Types",
    children: sidebarContent,
  };
  
  let mainPanelContent = <></>;
  let title = "Task Type";
  if (!ttId) {
    mainPanelContent = <TaskTypeForm />;
    title = "Create a Task Type";
  } else if (taskTypeQuery.isSuccess) {
    mainPanelContent = <TaskTypeShow taskType={taskTypeQuery.data} />;
    title = taskTypeQuery.data.name;
  }
  const mainPanelProps = {
    title,
    children: mainPanelContent,
  };

  return (
    <BasePageLayout mainPanelProps={mainPanelProps} sidebarProps={sidebarProps} />
  );
}