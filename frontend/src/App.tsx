import React from 'react';
import AppRoutes from './routes';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="app-shell">
      <AppRoutes />
    </div>
  );
};

export default App;
