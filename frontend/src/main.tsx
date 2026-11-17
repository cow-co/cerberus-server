import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router"
import './index.css'
import { CssBaseline } from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SigninPage from './pages/SigninPage.tsx'
import { store } from './state/store.ts'
import { Provider } from 'react-redux'
import UsersPage from './pages/UsersPage.tsx'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import ChangePasswordPage from './pages/ChangePasswordPage.tsx'
import TaskTypesPage from './pages/TaskTypesPage.tsx'
import ImplantsPage from './pages/ImplantsPage.tsx'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <ThemeProvider theme={darkTheme}>
    <StrictMode>
        <CssBaseline />
        <Provider store={store}>
          <QueryClientProvider client={queryClient}>
            <BrowserRouter>
              <Routes>
                <Route path="/" element={<ImplantsPage />} />
                <Route path="/signin" element={<SigninPage />} />
                <Route path="/change-password" element={<ChangePasswordPage />} />
                <Route path="users">
                  <Route index element={<UsersPage />} />
                  <Route path="view/*" element={<UsersPage />} />
                </Route>
                <Route path="task-types">
                  <Route index element={<TaskTypesPage />} />
                  <Route path="view/*" element={<TaskTypesPage />} />
                </Route>
              </Routes>
            </BrowserRouter>
          </QueryClientProvider>
        </Provider>
      </StrictMode>
  </ThemeProvider>
)
