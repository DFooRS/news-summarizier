import { Link } from 'react-router-dom';

export const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-md sticky top-0 z-10">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold hover:text-blue-200 transition-colors">
          Новостной агрегатор
        </Link>
        <div className="space-x-4">
          <Link
            to="/"
            className="text-lg hover:text-blue-200 transition-colors"
          >
            Главная
          </Link>
        </div>
      </div>
    </nav>
  );
};