import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://ai-lab-1-x6f6.onrender.com",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    config.withCredentials = true;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.error("Unauthorized access - redirecting to login");
    }
    return Promise.reject(error);
  }
);

export default apiClient;
