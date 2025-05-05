import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { fetchNewsDetail } from '../api/newsApi';
import { NewsItem } from '../types';
import { Button } from '../components/Button';
import { NewsDetailSkeleton } from '../components/Skeletons';

export const NewsDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [newsItem, setNewsItem] = useState<NewsItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadNewsDetail = async () => {
      try {
        if (!id) return;
        
        setLoading(true);
        const data = await fetchNewsDetail(parseInt(id));
        setNewsItem(data);
      } catch (err) {
        console.error('Failed to load news:', err);
        setError('Не удалось загрузить новость');
      } finally {
        setLoading(false);
      }
    };

    loadNewsDetail();
  }, [id]);

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
        <Button onClick={() => navigate('/')}>Вернуться на главную</Button>
      </div>
    );
  }

  if (loading || !newsItem) {
    return <NewsDetailSkeleton />;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Button 
        onClick={() => navigate(-1)} 
        className="mb-6"
        variant="outline"
      >
        ← Назад
      </Button>

      <article className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6">
          <h1 className="text-2xl md:text-3xl font-bold mb-4">{newsItem.title}</h1>
          
          <div className="flex items-center text-sm text-gray-500 mb-6">
            <span>{new Date(newsItem.created_at).toLocaleDateString()}</span>
            <span className="mx-2">•</span>
            <span>{newsItem.source}</span>
          </div>

          {newsItem.image && (
            <img 
              src={newsItem.image} 
              alt={newsItem.title}
              className="w-full h-64 object-cover mb-6 rounded"
            />
          )}

          <div className="prose max-w-none">
            <p className="text-lg font-medium text-gray-700 mb-4">{newsItem.summary}</p>
            <div className="border-t pt-4">
              <p className="whitespace-pre-line text-gray-800">{newsItem.content}</p>
            </div>
          </div>
        </div>
      </article>
    </div>
  );
};