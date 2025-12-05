import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Link, useNavigate } from "react-router-dom";
import { api } from "@/api/client";
import { useToast } from "@/components/ui/use-toast";

const Register = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const { toast } = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            await api.post('/register', { email, password });
            toast({
                title: "Success",
                description: "Registration successful! Please login.",
            });
            navigate("/login");
        } catch (error) {
            toast({
                variant: "destructive",
                title: "Error",
                description: "Registration failed. Email might be taken.",
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Create an Account</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? "Creating account..." : "Register"}
                        </Button>
                        <div className="text-center text-sm text-gray-500">
                            Already have an account?{" "}
                            <Link to="/login" className="text-blue-600 hover:underline">
                                Login
                            </Link>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
};

export default Register;
