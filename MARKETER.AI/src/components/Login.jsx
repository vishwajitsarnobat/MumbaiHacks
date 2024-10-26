import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { login as authLogin } from "../store/authSlice";
import { Button, Input, Logo } from "../components/index";
import authService from "../appwrite/auth";
import { useForm } from "react-hook-form";

function Login() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { register, handleSubmit } = useForm();
  const [error, setError] = useState("");

  const login = async (data) => {
    setError("");
    try {
      const session = await authService.login(data);
      if (session) {
        const userData = await authService.getCurrentUser();
        if (userData) dispatch(authLogin(userData));
        navigate("/");
      }
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="flex items-center justify-center w-full">
      <div className="mx-auto w-full max-w-lg p-10 rounded-xl bg-white shadow-lg">
        <div className="mb-2 flex justify-center">
          <span className="inline-block w-full max-w-[100px]">
            <Logo width="100%" />
          </span>
        </div>

        <h2 className="text-center text-2xl font-bold leading-tight text-zinc-900">
          Sign in to your account
        </h2>

        <p className="mt-2 text-center text-base text-zinc-600">
          Don&apos;t have an account?&nbsp;
          <Link
            to="/signup"
            className="font-medium text-blue-600 hover:text-blue-700 transition-colors"
          >
            Sign Up
          </Link>
        </p>

        {error && (
          <div className="mt-4 p-3 rounded-lg bg-red-50 border border-red-200">
            <p className="text-center text-red-600 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(login)} className="mt-8">
          <div className="space-y-5">
            <Input
              label="Email: "
              placeholder="Enter your email"
              type="email"
              {...register("email", {
                required: true,
                validate: {
                  matchPattern: (value) =>
                    /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(value) ||
                    "Email address must be a valid address",
                },
              })}
              className="w-full px-4 py-3 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 text-zinc-900 bg-white transition-colors"
            />

            <Input
              label="Password: "
              type="password"
              placeholder="Enter your password"
              {...register("password", { required: true })}
              className="w-full px-4 py-3 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 text-zinc-900 bg-white transition-colors"
            />

            <Button
              type="submit"
              className="w-full px-4 py-3 text-white bg-black hover:bg-black rounded-lg font-medium transition-colors focus:ring-2 focus:ring-blue-200 focus:ring-offset-2 align-middle"
            >
              Sign in
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
