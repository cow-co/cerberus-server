import React, { useEffect } from "react";
import Navbar from "./Navbar"
import Sidebar, { type SidebarProps } from "./Sidebar"
import MainPanel, { type MainPanelProps } from "./MainPanel";
import { Container } from "@mui/material";
import { useAppDispatch, useAppSelector } from "../../state/hooks";
import { useNavigate } from "react-router";
import { setAlertContent } from "../../state/alertSlice";

export interface PageProps {
  sidebarProps: SidebarProps;
  mainPanelProps: MainPanelProps;
  children?: React.ReactNode;
}


export default (props: PageProps) => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const username = useAppSelector(state => state.auth.username);
  const needsPWChange = useAppSelector(state => state.auth.requiresPWChange);
  
  useEffect(() => {
    dispatch(setAlertContent(null));
  }, []);
  useEffect(() => {
    if (!username) {
      navigate("/signin");
    } else if (needsPWChange) {
      navigate("/change-password");
    }
  }, [username, needsPWChange]);
  
  const {sidebarProps, mainPanelProps, children} = props;
  return (
    <Container sx={{m: 0, width: "100%", border: "none", maxWidth: "100vw !important"}}>
      <Navbar /> 
      <Sidebar {...sidebarProps} />
      <MainPanel {...mainPanelProps} />
      {children}
    </Container>
  )
}