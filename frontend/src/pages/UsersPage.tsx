import { useState } from "react";
import type { ResetPasswordResponse, UserResponse } from "../api/data-model/UserModels";
import BasePageLayout from "../components/layout/BasePageLayout";
import UserShow from "../components/user/UserShow";
import { useMutation, useQuery } from "@tanstack/react-query";
import { getUsers, resetPassword } from "../api/UserApi";
import AddIcon from "@mui/icons-material/Add";
import PasswordIcon from "@mui/icons-material/Password";
import {
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
} from "@mui/material";
import UserForm from "../components/user/UserForm";
import { setAlertContent } from "../state/alertSlice";
import { useAppDispatch } from "../state/hooks";

export default () => {
  const dispatch = useAppDispatch();
  const usersQuery = useQuery({ queryKey: ["users"], queryFn: getUsers });
  const [user, setUser] = useState<UserResponse | null>(null);
  const [formShown, setFormShown] = useState<boolean>(false);

  const pwdResetMutation = useMutation({
    mutationFn: resetPassword,
    onSuccess: (data: ResetPasswordResponse) => {
      dispatch(
        setAlertContent({
          alertContent: `${user?.username} password has been reset to ${data.new_password}`,
          alertType: "SUCCESS",
        }),
      );
    },
  });

  const sidebarContent = usersQuery.isSuccess ? (
    <List>
      {usersQuery.data!.map((user) => {
        return (
          <ListItem
            secondaryAction={
              <Tooltip describeChild title="Reset Password">
                <IconButton
                  edge="end"
                  onClick={() => {
                    setUser(user);
                    setFormShown(false);
                    pwdResetMutation.mutate(user.id);
                  }}
                >
                  <PasswordIcon />
                </IconButton>
              </Tooltip>
            }
            disablePadding
          >
            <ListItemButton
              onClick={() => {
                setFormShown(false);
                setUser(user);
              }}
              dense
            >
              <ListItemText primary={user.username} />
            </ListItemButton>
          </ListItem>
        );
      })}
      <ListItemButton
        onClick={() => {
          setUser(null);
          setFormShown(true);
        }}
      >
        <ListItemIcon>
          <AddIcon />
        </ListItemIcon>
        <ListItemText>Create</ListItemText>
      </ListItemButton>
    </List>
  ) : (
    <></>
  );
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
    <BasePageLayout
      mainPanelProps={mainPanelProps}
      sidebarProps={sidebarProps}
    />
  );
};
