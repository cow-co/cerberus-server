import { useState } from "react";
import type { UserResponse } from "../api/data-model/UserModels";
import BasePageLayout from "../components/layout/BasePageLayout";
import UserShow from "../components/user/UserShow";
import { useQuery } from "@tanstack/react-query";
import { getUsers } from "../api/UserApi";
import { List, ListItemButton, ListItemText } from "@mui/material";


export default () => {
  const usersQuery = useQuery({queryKey: ["users"], queryFn: getUsers});
  const [user, setUser] = useState<UserResponse|null>(null);
  

  const sidebarContent = usersQuery.isSuccess ? (<List>
    {usersQuery.data!.map(user => {
    return (
      <ListItemButton onClick={() => setUser(user)}>
        <ListItemText>{user.username}</ListItemText>
      </ListItemButton>
    );
  })}
  </List>) : <></>;
  const sidebarProps = {
    title: "Users",
    children: sidebarContent,
  };

  const mainPanelContent = user ? <UserShow user={user} /> : <></>;
  const mainPanelProps = {
    title: user ? user.username : "User",
    children: mainPanelContent,
  };

  return (
    <BasePageLayout mainPanelProps={mainPanelProps} sidebarProps={sidebarProps} />
  );
}