import axios from "axios";

const API = "http://127.0.0.1:8000";
const api = axios.create({ baseURL: API });

export const registerUser = (data) => api.post("/register", data);
export const loginUser = (data) => api.post("/login", data);
