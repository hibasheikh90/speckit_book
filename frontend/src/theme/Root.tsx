import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';

// Root component wraps the entire application
// This is where we add global providers that need to be available everywhere
export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
