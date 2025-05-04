import React, { createContext, useState, useEffect, useContext } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      fetchUserProfile(token);
    } else {
      setUser(null);
    }
  }, [token]);

  const fetchUserProfile = async (token) => {
    try {
      const res = await fetch("/api/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) throw new Error("Token inválido");
      const data = await res.json();
      console.log("Perfil do usuário carregado:", data); // Log para depuração
      setUser(data);
    } catch {
      console.error("Erro ao carregar perfil do usuário:", error);
      logout();
    }
  };

  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append("email", username);
    formData.append("password", password);

    const res = await fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });

    if (!res.ok) {
      throw new Error("Login falhou");
    }

    const data = await res.json();
    setToken(data.access_token);
    localStorage.setItem("token", data.access_token);
  };

  const register = async (userData) => {
    const res = await fetch("https://know-your-fan-production-c1f0.up.railway.app/submit-user-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Alterado para application/json
      },
      body: JSON.stringify(userData),
    });
  
    if (!res.ok) {
      throw new Error("Cadastro falhou");
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider value={{ token, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}