import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchNewsList } from '../api/newsApi';
import { NewsItem } from '../types';
import { Pagination } from '../components/Pagination';
import { NewsSkeleton } from '../components/Skeletons';

export const Home = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    const loadNews = async () => {
      try {
        setLoading(true);
        const allNews = await fetchNewsList();
        setNews(allNews);
        setTotalPages(Math.ceil(allNews.length / itemsPerPage));
      } catch (error) {
        console.error('Error loading news:', error);
      } finally {
        setLoading(false);
      }
    };

    loadNews();
  }, []);

  // Получаем новости для текущей страницы
  const currentNews = news.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">Новостной агрегатор</h1>
      
      {loading ? (
        <div className="space-y-6">
          {[...Array(itemsPerPage)].map((_, i) => (
            <NewsSkeleton key={i} />
          ))}
        </div>
      ) : (
        <>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {currentNews.map((item) => (
              <div key={item.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="p-6">
                  <h2 className="text-xl font-semibold mb-2 line-clamp-2">{item.title}</h2>
                  <p className="text-gray-600 mb-4 line-clamp-3">{item.summary}</p>
                  <Link
                    to={`/news/${item.id}`}
                    className="inline-block text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Читать далее →
                  </Link>
                </div>
                <div className="px-6 py-4 bg-gray-50 border-t">
                  <span className="text-sm text-gray-500">
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="mt-8 flex justify-center">
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            </div>
          )}
        </>
      )}
    </div>
  );
};