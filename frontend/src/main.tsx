import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router"
import './index.css'
import App from './App.tsx'
import { CssBaseline } from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SigninPage from './pages/SigninPage.tsx'
import { store } from './state/store.ts'
import { Provider } from 'react-redux'
import UsersPage from './pages/UsersPage.tsx'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

createRoot(document.getElementById('root')!).render(
  <ThemeProvider theme={darkTheme}>
    <StrictMode>
        <CssBaseline />
        <Provider store={store}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<App />} />
              <Route path="/signin" element={<SigninPage />} />
              <Route path="/users" element={<UsersPage />} />
              <Route path="/task-types" />
            </Routes>
          </BrowserRouter>
        </Provider>
      </StrictMode>
  </ThemeProvider>
)
