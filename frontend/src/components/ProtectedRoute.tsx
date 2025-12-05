import { useAuth } from "@/context/AuthContext";
import { Navigate } from "react-router-dom";

export const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const { token, isLoading } = useAuth();

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!token) {
        return <Navigate to="/login" />;
    }

    return <>{children}</>;
};
