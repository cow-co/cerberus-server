import { Paper, Table, TableBody, TableCell, TableContainer, TableRow } from "@mui/material";
import type { UserResponse } from "../../api/data-model/UserModels";


export interface ShowUserProps {
  user: UserResponse;
};


export default (props: ShowUserProps) => {
  const {user} = props;
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }}>
        <TableBody>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>{user.id}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>{user.username}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Is Enabled?</TableCell>
            <TableCell>{user.is_locked ? "❌" : "✅"}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Role</TableCell>
            <TableCell>{user.role}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
}