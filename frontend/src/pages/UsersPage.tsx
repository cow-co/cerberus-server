import { useState } from "react";
import type { UserResponse } from "../api/data-model/UserModels";
import BasePageLayout from "../components/layout/BasePageLayout";
import UserShow from "../components/user/UserShow";
import { useQuery } from "@tanstack/react-query";
import { getUsers } from "../api/UserApi";
import AddIcon from '@mui/icons-material/Add';
import { List, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import UserForm from "../components/user/UserForm";


export default () => {
  const usersQuery = useQuery({queryKey: ["users"], queryFn: getUsers});
  const [user, setUser] = useState<UserResponse|null>(null);
  const [formShown, setFormShown] = useState<boolean>(false);

  const sidebarContent = usersQuery.isSuccess ? (
    <List>
      {usersQuery.data!.map(user => {
        return (
          <ListItemButton onClick={() => {
              setFormShown(false);
              setUser(user);
            }}>
            <ListItemText>{user.username}</ListItemText>
          </ListItemButton>
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