// hooks/useAuth.js
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, signup } from "../services/authService";
import { useAuthStore } from "../store/authStore";
import toast from "react-hot-toast";

const useAuth = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { setTokens, logout: storeLogout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = async (email, password) => {
    setIsLoading(true);
    try {
      const { accessToken, refreshToken } = await login(email, password);
      setTokens(accessToken, refreshToken);
      navigate("/dashboard");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Login failed. Check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignup = async (email, password, name) => {
    setIsLoading(true);
    try {
      await signup(email, password, name);
      toast.success("Account created! Please log in.");
      navigate("/login");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Signup failed. Try a different email.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    storeLogout();
    navigate("/login");
  };

  return { handleLogin, handleSignup, handleLogout, isLoading };
};

export default useAuth;
