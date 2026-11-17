import { useState } from "react";
import BasePageLayout from "../components/layout/BasePageLayout";
import { useQuery } from "@tanstack/react-query";
import { Dialog, DialogContent, DialogTitle, List, ListItemButton, ListItemText } from "@mui/material";
import { getImplants } from "../api/ImplantApi";
import { type ImplantResponse } from "../api/data-model/ImplantModels";
import ImplantShow from "../components/implant/ImplantShow";
import TaskForm from "../components/task/TaskForm";
import { type TaskResponse } from "../api/data-model/TaskModels";
import TaskShow from "../components/task/TaskShow";


export default () => {
  const implantsQuery = useQuery({queryKey: ["implants"], queryFn: getImplants});
  const [implant, setImplant] = useState<ImplantResponse|null>(null);
  const [addModalOpen, setAddModalOpen] = useState<boolean>(false);
  const [viewModalOpen, setViewModalOpen] = useState<boolean>(false);
  const [selectedTask, setSelectedTask] = useState<TaskResponse|null>(null);

  const impIdent = (imp: ImplantResponse): string => {
    let implantIdentifier = imp.implant_id;
    if (imp.hostname) {
      implantIdentifier = imp.hostname;
    } else if (imp.ip_addr) {
      implantIdentifier = imp.ip_addr;
    }
    return implantIdentifier;
  }

  const implantIdentifier = implant ? impIdent(implant) : "";

  const sidebarContent = implantsQuery.isSuccess ? (
    <List>
      {implantsQuery.data!.map(imp => {
        imp
        return (
          <ListItemButton onClick={() => {
              setImplant(imp);
            }}>
            <ListItemText>{impIdent(imp)} ({imp.is_active ? "Active" : "Inactive"})</ListItemText>
          </ListItemButton>
        );
      })}
    </List>
  ) : <></>;
  const sidebarProps = {
    title: "Implants",
    children: sidebarContent,
  };

  let mainPanelContent = <></>;
  if (implant) {
    mainPanelContent = <ImplantShow 
      implant={implant} 
      onAddTask={() => setAddModalOpen(true)} 
      onSelectTask={(task) => {
        setSelectedTask(task);
        setViewModalOpen(true);
      }
    }/>;
  }
  const mainPanelProps = {
    title: implantIdentifier ? implantIdentifier : "Implant",
    children: mainPanelContent,
  };

  return (
    <>
      <BasePageLayout mainPanelProps={mainPanelProps} sidebarProps={sidebarProps} />
      <Dialog open={addModalOpen} onClose={() => setAddModalOpen(false)}>
        <DialogTitle>Create a Task</DialogTitle>
        <DialogContent>
          <TaskForm implant_id={implant?.implant_id} />
        </DialogContent>
      </Dialog>
      <Dialog open={viewModalOpen} onClose={() => setViewModalOpen(false)}>
        <DialogTitle>Task {selectedTask?.name}</DialogTitle>
        <DialogContent>
          <TaskShow task={selectedTask} />
        </DialogContent>
      </Dialog>
    </>
    
  );
}