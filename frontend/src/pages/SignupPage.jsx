import { useState } from "react";
import { Link }     from "react-router-dom";
import useAuth      from "../hooks/useAuth";
import Input        from "../components/common/Input";
import Button       from "../components/common/Button";
import ThemeToggle  from "../components/common/ThemeToggle";

const SignupPage = () => {
  const [email, setEmail]       = useState("");
  const [name, setName]         = useState("");
  const [password, setPassword] = useState("");
  const { handleSignup, isLoading } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSignup(email, password, name);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col items-center justify-center px-4">
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 w-full max-w-sm">
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-1">Create Account</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">Join HIStock today.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Full Name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Jane Doe"
            required
          />
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
          />
          <Button type="submit" isLoading={isLoading} className="w-full mt-2">
            Sign up
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignupPage;
