import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

export const registerUser = (data) => api.post("/register", data);
export const loginUser = (data) => api.post("/login", data);