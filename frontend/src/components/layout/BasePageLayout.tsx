import React from "react";
import Navbar from "./Navbar"
import Sidebar, { type SidebarProps } from "./Sidebar"
import MainPanel, { type MainPanelProps } from "./MainPanel";
import { Container } from "@mui/material";

export interface PageProps {
  sidebarProps: SidebarProps;
  mainPanelProps: MainPanelProps;
  children?: React.ReactNode;
}


export default (props: PageProps) => {
  // TODO Redirect to login if no username set in state
  const {sidebarProps, mainPanelProps, children} = props;
  return (
    <Container sx={{m: 0, width: "100%", border: "none"}}>
      <Navbar /> 
      <Sidebar {...sidebarProps} />
      <MainPanel {...mainPanelProps} />
      {children}
    </Container>
  )
}