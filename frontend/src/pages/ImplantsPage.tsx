import { useState } from "react";
import BasePageLayout from "../components/layout/BasePageLayout";
import { useQuery } from "@tanstack/react-query";
import { Button, List, ListItem, ListItemButton, ListItemText } from "@mui/material";
import { getImplants } from "../api/ImplantApi";
import type { ImplantResponse } from "../api/data-model/ImplantModels";


export default () => {
  const implantsQuery = useQuery({queryKey: ["implants"], queryFn: getImplants});
  const [implant, setImplant] = useState<ImplantResponse|null>(null);

  let implantIdentifier = implant?.implant_id;
  if (implant?.hostname) {
    implantIdentifier = implant.hostname;
  } else if (implant?.ip_addr) {
    implantIdentifier = implant.ip_addr;
  }

  const sidebarContent = implantsQuery.isSuccess ? (
    <List>
      {implantsQuery.data!.map(imp => {
        return (
          <ListItem secondaryAction={<Button variant="contained" onClick={() => {
            setImplant(imp);
          }}>Reset Password</Button>}>
            <ListItemButton onClick={() => {
                setImplant(imp);
              }}>
              <ListItemText>{implantIdentifier}</ListItemText>
            </ListItemButton>
          </ListItem>
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
    mainPanelContent = <ImplantShow implant={implant} />;
  }
  const mainPanelProps = {
    title: implantIdentifier ? implantIdentifier : "Implant",
    children: mainPanelContent,
  };

  return (
    <BasePageLayout mainPanelProps={mainPanelProps} sidebarProps={sidebarProps} />
  );
}