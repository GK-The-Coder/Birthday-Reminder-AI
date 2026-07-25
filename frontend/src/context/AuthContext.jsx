import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser, registerUser } from "../services/authApi";
import { AuthContext } from "./AuthContextDefinition";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token") || null);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  const register = async (data) => {
    const response = await registerUser(data);
    return response;
  };

  const login = async (data) => {
    const response = await loginUser(data);
    const accessToken = response.data?.access_token;
    if (accessToken) {
      setToken(accessToken);
      navigate("/");
    }
    return response;
  };

  const logout = () => {
    setToken(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ token, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
