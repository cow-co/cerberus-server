import { useState } from "react";
import type { UserResponse } from "../api/data-model/UserModels";
import BasePageLayout from "../components/layout/BasePageLayout";
import UserShow from "../components/user/UserShow";
import { useMutation, useQuery } from "@tanstack/react-query";
import { getUsers, resetPassword } from "../api/UserApi";
import AddIcon from '@mui/icons-material/Add';
import { Button, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import UserForm from "../components/user/UserForm";
import { setAlertContent } from "../state/alertSlice";
import { useAppDispatch } from "../state/hooks";


export default () => {
  const dispatch = useAppDispatch();
  const usersQuery = useQuery({queryKey: ["users"], queryFn: getUsers});
  const [user, setUser] = useState<UserResponse|null>(null);
  const [formShown, setFormShown] = useState<boolean>(false);
  
  const pwdResetMutation = useMutation({
    mutationFn: resetPassword,
    onSuccess: (data: string) => {
      dispatch(setAlertContent({
        alertContent: `${user?.username} password has been reset to ${data}`,
        alertType: "SUCCESS",
      }));
    },
  });

  const sidebarContent = usersQuery.isSuccess ? (
    <List>
      {usersQuery.data!.map(user => {
        return (
          <ListItem secondaryAction={<Button variant="contained" onClick={() => {
            setUser(user);
            setFormShown(false);
            pwdResetMutation.mutate(user.id);
          }}>Reset Password</Button>}>
            <ListItemButton onClick={() => {
                setFormShown(false);
                setUser(user);
              }}>
              <ListItemText>{user.username}</ListItemText>
            </ListItemButton>
          </ListItem>
        );
      })}
      <ListItemButton onClick={() => {
        setUser(null);
        setFormShown(true);
      }}>
        <ListItemIcon><AddIcon /></ListItemIcon>
        <ListItemText>Create</ListItemText>
      </ListItemButton>
    </List>
  ) : <></>;
  const sidebarProps = {
    title: "Users",
    children: sidebarContent,
  };

  let mainPanelContent = <></>;
  if (user) {
    mainPanelContent = <UserShow user={user} />;
  } else if (formShown) {
    mainPanelContent = <UserForm />;
  }
  const mainPanelProps = {
    title: user ? user.username : "User",
    children: mainPanelContent,
  };

  return (
    <BasePageLayout mainPanelProps={mainPanelProps} sidebarProps={sidebarProps} />
  );
}