import { useState } from "react";
import BasePageLayout from "../components/layout/BasePageLayout";
import { useQuery } from "@tanstack/react-query";
import { List, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import type { TaskTypeResponse } from "../api/data-model/TaskModels";
import { getTaskTypes } from "../api/TaskApi";
import TaskTypeShow from "../components/task/TaskTypeShow";


export default () => {
  const taskTypesQuery = useQuery({queryKey: ["taskTypes"], queryFn: getTaskTypes});
  const [taskType, setTaskType] = useState<TaskTypeResponse|null>(null);
  const [formShown, setFormShown] = useState<boolean>(false);

  const sidebarContent = taskTypesQuery.isSuccess ? (
    <List>
      {taskTypesQuery.data!.map(tt => {
        return (
        <ListItemButton onClick={() => {
          setTaskType(tt);
          }}>
          <ListItemText>tt.name</ListItemText>
        </ListItemButton>
        );
      })}
      <ListItemButton onClick={() => {
        setTaskType(null);
        setFormShown(true);
      }}>
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
    if (taskType) {
      mainPanelContent = <TaskTypeShow taskType={taskType} />;
    } else if (formShown) {
      mainPanelContent = <TaskTypeForm />;
    }
  const mainPanelProps = {
    title: taskType ? taskType.name : "Task Type",
    children: mainPanelContent,
  };

  return (
    <BasePageLayout mainPanelProps={mainPanelProps} sidebarProps={sidebarProps} />
  );
}