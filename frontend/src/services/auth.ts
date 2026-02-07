import { api } from "../lib/api";


export const registerUser = async (email: string, password: string) => {
  const res = await api.post("/auth/register", {
    email,
    password,
  });
  return res.data;
};

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
  };
}

export const loginUser = async (
  email: string,
  password: string
): Promise<LoginResponse> => {
  const res = await api.post("/auth/login", { email, password });
  return res.data;
};

export const signupUser = async (
  email: string,
  password: string
): Promise<{ message: string }> => {
  const res = await api.post("/auth/signup", { email, password });
  return res.data;
};

export const getMe = async () => {
  const res = await api.get("/auth/me");
  return res.data;
};
