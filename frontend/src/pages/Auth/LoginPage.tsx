import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { authApi } from '../../api/services';
import { Shield, Lock, User as UserIcon } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const setToken = useAuthStore((state) => state.setToken);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const res = await authApi.login(formData);
      setToken(res.data.access_token);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка авторизации');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bt-bg flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-bt-card border border-bt-border rounded-lg p-6 shadow-xl">
        <div className="flex items-center justify-center gap-3 mb-6">
          <Shield className="w-8 h-8 text-bt-amber" />
          <h1 className="text-xl font-bold text-white tracking-wide">
            DRCM TERMINAL <span className="text-bt-amber text-xs">v0.2</span>
          </h1>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-bt-red text-red-200 text-sm rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs uppercase font-bold text-slate-400 mb-1">
              Позывной Командира
            </label>
            <div className="relative">
              <UserIcon className="w-5 h-5 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-slate-900 border border-bt-border rounded pl-10 pr-3 py-2 text-white focus:outline-none focus:border-bt-amber"
                placeholder="Commander"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs uppercase font-bold text-slate-400 mb-1">
              Пароль
            </label>
            <div className="relative">
              <Lock className="w-5 h-5 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-900 border border-bt-border rounded pl-10 pr-3 py-2 text-white focus:outline-none focus:border-bt-amber"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-bt-amber hover:bg-amber-600 text-slate-950 font-bold py-2 px-4 rounded transition-colors disabled:opacity-50"
          >
            {isLoading ? 'Подключение...' : 'Вход в терминал'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate-400">
          Нет аккаунта?{' '}
          <Link to="/register" className="text-bt-amber hover:underline">
            Зарегистрировать отряд
          </Link>
        </p>
      </div>
    </div>
  );
};