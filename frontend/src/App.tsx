import { Box } from '@mui/material';
import BasePageLayout from './components/layout/BasePageLayout'
import type { MainPanelProps } from './components/layout/MainPanel';
import type { SidebarProps } from './components/layout/Sidebar';

function App() {
  const sideContent = <></>;
  const mainContent = (<Box sx={{ display: 'flex', flex: 1, width: '100%' }}>
    
  </Box>);

  const sidebarProps: SidebarProps = {
    children: sideContent,
    title: "test"
  };

  const mainPanelProps: MainPanelProps = {
    children: mainContent,
    title: "test"
  };

  return (
    <BasePageLayout sidebarProps={sidebarProps} mainPanelProps={mainPanelProps} />
  );
}

export default App;
