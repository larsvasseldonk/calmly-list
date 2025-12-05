import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

interface User {
    id: string;
    email: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const initAuth = async () => {
            if (token) {
                try {
                    // We could add a /me endpoint to validate token and get user details
                    // For now, we'll just decode the token or assume it's valid if we have it
                    // Ideally: const userData = await api.get('/users/me'); setUser(userData);

                    // Since we don't have a /me endpoint yet, we'll just set a dummy user or extract from token if possible
                    // But for now, let's just assume logged in if token exists.
                    // A better approach is to actually fetch the user.
                    // Let's rely on the fact that if API calls fail with 401, we logout.
                    setUser({ id: 'current', email: 'user@example.com' }); // Placeholder until we have /me
                } catch (error) {
                    logout();
                }
            }
            setIsLoading(false);
        };

        initAuth();
    }, [token]);

    const login = (newToken: string) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
        // In a real app, we'd fetch user details here
        setUser({ id: 'current', email: 'user@example.com' });
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
