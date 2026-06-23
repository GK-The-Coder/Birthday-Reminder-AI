import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export const getBirthdays = () => api.get("/birthdays");
export const addBirthday = (data) => api.post("/birthdays", data);
export const deleteBirthday = (id) => api.delete(`/birthdays/${id}`);
export const updateBirthday = (id, data) => api.put(`/birthdays/${id}`, data);

export const generateWish = (name) =>
  api.post("/generate-wish", { name });

export const sendBirthdayEmail = (data) =>
  api.post("/send-birthday-email", data);

export const getStats = () => api.get("/stats");
export const getLogs = () => api.get("/email-logs");