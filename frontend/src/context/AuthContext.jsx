import React, { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const navigate = useNavigate()

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      const storedToken = localStorage.getItem('token')
      if (storedToken) {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${storedToken}`
            }
          })
          
          if (response.ok) {
            const userData = await response.json()
            setUser(userData)
            setToken(storedToken)
          } else {
            // Token is invalid, clear it
            localStorage.removeItem('token')
            setToken(null)
            setUser(null)
          }
        } catch (error) {
          console.error('Auth check failed:', error)
          localStorage.removeItem('token')
          setToken(null)
          setUser(null)
        }
      }
      setLoading(false)
    }

    checkAuth()
  }, [])

  const login = async (email, password) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const data = await response.json()
      const accessToken = data.access_token

      // Store token
      localStorage.setItem('token', accessToken)
      setToken(accessToken)

      // Get user info
      const userResponse = await fetch('http://127.0.0.1:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      })

      if (userResponse.ok) {
        const userData = await userResponse.json()
        setUser(userData)
        navigate('/dashboard')
        return { success: true }
      }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, error: error.message }
    }
  }

  const logout = async () => {
    try {
      if (token) {
        await fetch('http://127.0.0.1:8000/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('token')
      setToken(null)
      setUser(null)
      navigate('/')
    }
  }

  const register = async (email, password, full_name, role = 'officer') => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password, full_name, role })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Registration failed')
      }

      const userData = await response.json()
      return { success: true, data: userData }
    } catch (error) {
      console.error('Registration error:', error)
      return { success: false, error: error.message }
    }
  }

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
    register
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
