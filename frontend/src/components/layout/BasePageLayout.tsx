import type React from "react";
import Navbar from "./Navbar"
import Sidebar, { type SidebarProps } from "./Sidebar"
import MainPanel, { type MainPanelProps } from "./MainPanel";

export interface PageProps {
  sidebarProps: SidebarProps;
  mainPanelProps: MainPanelProps;
  children?: React.ReactNode;
}


export default (props: PageProps) => {
  const {sidebarProps, mainPanelProps, children} = props;
  return (
    <>
      <Navbar /> 
      <Sidebar {...sidebarProps} />
      <MainPanel {...mainPanelProps} />
      {children}
    </>
  )
}