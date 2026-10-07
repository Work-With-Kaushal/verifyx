import axios from "axios";

const API = axios.create({
  baseURL: "https://verifyx-backend-s31f.onrender.com"
});

export default API;