import { Container, Typography } from "@mui/material";
import type React from "react"

export interface MainPanelProps {
  children: React.ReactNode;
  title: string;
}


export default (props: MainPanelProps) =>{
  const {children, title} = props;
  return (
    <Container maxWidth="lg">
      <Typography variant="h2">{title}</Typography>
      {children}
    </Container>
  );
}