import {
  Box,
  Card,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Typography,
} from "@mui/material";
import type { ImplantResponse } from "../../api/data-model/ImplantModels";
import { getImplantTasks } from "../../api/ImplantApi";
import { useQuery } from "@tanstack/react-query";
import type { TaskResponse } from "../../api/data-model/TaskModels";
import AddIcon from '@mui/icons-material/Add';

export interface ShowImplantProps {
  implant: ImplantResponse;
  onAddTask:  () => void,
  onSelectTask: (task: TaskResponse) => void,
}

export default (props: ShowImplantProps) => {
  const { implant, onAddTask, onSelectTask } = props;
  const tasksQuery = useQuery({queryKey: ["implantTasks", implant.implant_id], queryFn: () => getImplantTasks(implant.implant_id)});
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
        <Stack spacing={2}>
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
          <Typography variant="h6">Tasks Assigned</Typography>
          <List>
            {tasksQuery.data?.map(task => <ListItemButton onClick={() => onSelectTask(task)}><ListItemText primary={task.name} secondary={
                <>
                  {task.}
                </>
              }  /></ListItemButton>)}
            <ListItemButton onClick={onAddTask}>
              <ListItemIcon><AddIcon /></ListItemIcon>
              <ListItemText primary="Queue a New Task"/>
            </ListItemButton>
          </List>
        </Stack>
      </Card>
    </Box>
  );
};
