import React, { createContext, useContext, useState, useEffect } from 'react'

const AppContext = createContext()

export const AppProvider = ({ children }) => {
  // ---- Global States ----
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token') || null)
  const [loading, setLoading] = useState(false)
  const [refreshFlag, setRefreshFlag] = useState(false)

  // ---- Login Function ----
  const login = (userData, jwtToken) => {
    setUser(userData)
    setToken(jwtToken)
    localStorage.setItem('token', jwtToken)
  }

  // ---- Logout Function ----
  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
  }

  // ---- Toggle refresh trigger (useful for updating dashboard) ----
  const triggerRefresh = () => {
    setRefreshFlag(!refreshFlag)
  }

  // ---- Load user from token (optional future use) ----
  useEffect(() => {
    if (token) {
      // In real app, fetch user profile from backend
      setUser({ name: "Traffic Officer", role: "admin" })
    }
  }, [token])

  return (
    <AppContext.Provider
      value={{
        user,
        token,
        loading,
        setLoading,
        login,
        logout,
        refreshFlag,
        triggerRefresh
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

// ---- Custom Hook for Context Access ----
export const useAppContext = () => useContext(AppContext)
