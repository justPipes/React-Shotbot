import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL;

export const fetchData = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/data`);
  return response.data;
};