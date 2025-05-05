import axios from 'axios';
import { NewsItem } from '../types';

const API_URL = 'http://localhost:8000/api';

export const fetchNewsList = async (): Promise<NewsItem[]> => {
  try {
    const response = await axios.get(`${API_URL}/news`);
    return response.data;
  } catch (error) {
    console.error('Error fetching news list:', error);
    return [];
  }
};

export const fetchNewsDetail = async (id: number): Promise<NewsItem> => {
  try {
    const response = await axios.get(`${API_URL}/news/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching news detail:', error);
    throw error;
  }
};