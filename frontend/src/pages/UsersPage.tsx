import type { ResetPasswordResponse, UserResponse } from "../api/data-model/UserModels";
import BasePageLayout from "../components/layout/BasePageLayout";
import UserShow from "../components/user/UserShow";
import { useMutation, useQuery } from "@tanstack/react-query";
import { getUser, getUsers, resetPassword } from "../api/UserApi";
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
import { useLocation } from "react-router";

const generateUserQuery = (userId: string | undefined) => {
  return useQuery({
    queryFn: (): Promise<UserResponse> => {
      if (userId) {
        return getUser(userId);
      } else {
        return Promise.reject("No userId provided");
      }
    },
    queryKey: ["user", userId],
  })
}

export default () => {
  const loc = useLocation();
  const path_elements = loc.pathname.split("/");
  const userId = path_elements.at(-1);
  const dispatch = useAppDispatch();
  const usersQuery = useQuery({ queryKey: ["users"], queryFn: getUsers });
  const userQuery = generateUserQuery(userId);

  const pwdResetMutation = useMutation({
    mutationFn: resetPassword,
    onSuccess: (data: ResetPasswordResponse) => {
      dispatch(
        setAlertContent({
          alertContent: `Password has been reset to ${data.new_password}`,
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
              href={`/users/view/${user.id}`}
              dense
            >
              <ListItemText primary={user.username} />
            </ListItemButton>
          </ListItem>
        );
      })}
      <ListItemButton href="/users">
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
  let title = "User";
  if (!userId) {
    mainPanelContent = <UserForm />;
    title = "Create a User";
  } else if (userQuery.isSuccess) {
    mainPanelContent = <UserShow user={userQuery.data} />;
    title = userQuery.data.username;
  }
  const mainPanelProps = {
    title,
    children: mainPanelContent,
  };

  return (
    <BasePageLayout
      mainPanelProps={mainPanelProps}
      sidebarProps={sidebarProps}
    />
  );
};
