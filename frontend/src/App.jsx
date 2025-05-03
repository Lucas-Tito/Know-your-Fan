import { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import './App.css';

import { AuthProvider, AuthContext } from './features/auth/AuthProvider';
import PrivateRoute from './features/auth/PrivateRoute';
import LoginForm from './features/auth/LoginForm';

import DocumentUpload from './features/validation/DocumentUpload';
import EsportsProfile from './features/validation/EsportsProfile';
import BlueskyConnect from './features/social/BlueskyConnect';
import SocialMediaIntegration from './features/social/SocialMediaIntegration';

const Dashboard = () => {
  const tabs = [
    { name: "Perfil", path: "profile" },
    { name: "Documentos", path: "documents" },
    { name: "E-sports", path: "esports" },
    { name: "Redes Sociais", path: "social" },
    { name: "Bluesky", path: "bluesky" }
  ];

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-blue-800 text-white p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Know Your Fan</h1>
          <LogoutButton />
        </div>
      </header>

      <nav className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4">
          <ul className="flex overflow-x-auto">
            {tabs.map((tab) => (
              <li key={tab.path} className="mr-1">
                <Link
                  to={`/dashboard/${tab.path}`}
                  className="inline-block px-4 py-3 hover:text-blue-600 hover:border-blue-600 border-b-2 border-transparent"
                >
                  {tab.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </nav>

      <main className="py-6 px-4">
        <Routes>
          <Route path="profile" element={<UserProfile />} />
          <Route path="documents" element={<DocumentUpload />} />
          <Route path="esports" element={<EsportsProfile />} />
          <Route path="social" element={<SocialMediaIntegration />} />
          <Route path="bluesky" element={<BlueskyConnect />} />
          <Route path="*" element={<Navigate to="profile" replace />} />
        </Routes>
      </main>
    </div>
  );
};

const LogoutButton = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 bg-red-600 rounded hover:bg-red-700 transition"
    >
      Logout
    </button>
  );
};

// Você precisa definir UserProfile ou importar se já existir
const UserProfile = () => {
  return <div>Perfil do Usuário (implemente aqui)</div>;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route 
            path="/dashboard/*" 
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } 
          />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;