import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api, token } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  const logout = useCallback(() => {
    token.clear();
    setUser(null);
  }, []);

  useEffect(() => {
    if (!token.get()) return setReady(true);
    api("/auth/me")
      .then(setUser)
      .catch(logout)
      .finally(() => setReady(true));
  }, [logout]);

  useEffect(() => {
    window.addEventListener("carpool:logout", logout);
    return () => window.removeEventListener("carpool:logout", logout);
  }, [logout]);

  const signIn = (res) => {
    token.set(res.access_token);
    setUser(res.user);
  };

  return <AuthContext.Provider value={{ user, ready, signIn, logout }}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
