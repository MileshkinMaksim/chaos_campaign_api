import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { LoginPage } from './pages/Auth/LoginPage';
import { RegisterPage } from './pages/Auth/RegisterPage';
import { ForceCreationPage } from './pages/ForceWizard/ForceCreationPage';
import { DashboardPage } from './pages/Dashboard/DashboardPage';
import { ForceSelectionPage } from './pages/ForceSelection/ForceSelectionPage';

const queryClient = new QueryClient();

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Защищенные маршруты */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<ForceSelectionPage />} />
            <Route path="/forces/create" element={<ForceCreationPage />} />
            <Route path="/forces/:id" element={<DashboardPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;