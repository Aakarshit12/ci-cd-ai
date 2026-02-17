import axios from "axios";

// TEMP: debug what base URL gets baked into the bundle

console.log("API BASE URL:", import.meta.env.VITE_API_BASE_URL);

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});
