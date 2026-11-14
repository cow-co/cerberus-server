import {
  Box,
  Card,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
} from "@mui/material";
import type { ImplantResponse } from "../../api/data-model/ImplantModels";

export interface ShowImplantProps {
  implant: ImplantResponse;
}

export default (props: ShowImplantProps) => {
  const { implant } = props;
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Card
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "60%",
        }}
      >
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }}>
            <TableBody>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>{implant.implant_id}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Hostname</TableCell>
                <TableCell>{implant.hostname ? implant.hostname : "UNKNOWN"}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>IP Address</TableCell>
                <TableCell>{implant.ip_addr ? implant.ip_addr : "UNKNOWN"}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Implant Version</TableCell>
                <TableCell>{implant.major_ver}.{implant.minor_ver}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Is Active?</TableCell>
                <TableCell>{implant.is_active ? "❌" : "✅"}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Card>
    </Box>
  );
};
