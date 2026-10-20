import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { forcesApi } from '../../api/services';
import { useAuthStore } from '../../store/authStore';
import { 
  Shield, 
  PlusCircle, 
  Coins, 
  Award, 
  Crosshair, 
  Users, 
  ArrowRight, 
  LogOut,
  Trash2
} from 'lucide-react';

export const ForceSelectionPage: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const logout = useAuthStore((state) => state.logout);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const { data: forces, isLoading, error } = useQuery({
    queryKey: ['my-forces'],
    queryFn: () => forcesApi.getMyForces(),
  });

  // Мутация удаления отряда
  const deleteMutation = useMutation({
    mutationFn: (forceId: string) => forcesApi.deleteForce(forceId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my-forces'] });
      setDeletingId(null);
    },
    onError: (err) => {
      console.error("Ошибка при удалении отряда:", err);
      alert("Не удалось удалить отряд. Попробуйте еще раз.");
      setDeletingId(null);
    }
  });

  const handleDelete = (e: React.MouseEvent, forceId: string, forceName: string) => {
    e.stopPropagation(); // Предотвращаем переход на страницу отряда при клике на корзину
    if (window.confirm(`Вы уверены, что хотите расформировать отряд "${forceName}"? Вся техника и пилоты будут удалены из базы данных.`)) {
      setDeletingId(forceId);
      deleteMutation.mutate(forceId);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bt-bg text-white flex items-center justify-center font-mono">
        <p className="text-bt-amber animate-pulse">Загрузка реестра ваших отрядов...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bt-bg text-white p-6 flex flex-col items-center">
      <div className="w-full max-w-6xl">
        {/* Шапка */}
        <div className="flex justify-between items-center mb-8 border-b border-bt-border pb-4">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-bt-amber" />
            <div>
              <h1 className="text-2xl font-bold tracking-wider uppercase text-white">
                Командный Штаб
              </h1>
              <p className="text-xs text-slate-400">Выберите активный отряд или сформируйте новый</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-1.5 bg-red-950/60 hover:bg-red-900 border border-bt-red/40 text-red-300 font-bold px-3 py-2 rounded text-xs transition-colors"
          >
            <LogOut className="w-4 h-4" /> Выход
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-900/50 border border-bt-red rounded text-red-200 text-sm">
            Не удалось загрузить список отрядов. Проверьте соединение с сервером.
          </div>
        )}

        {/* Сетка отрядов */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Карточка создания нового отряда */}
          <Link
            to="/forces/create"
            className="bg-bt-card/50 hover:bg-bt-card border-2 border-dashed border-bt-border hover:border-bt-amber rounded-xl p-6 shadow-lg transition-all flex flex-col items-center justify-center text-center gap-3 min-h-[220px] group"
          >
            <div className="w-12 h-12 rounded-full bg-slate-900 border border-bt-border flex items-center justify-center group-hover:border-bt-amber group-hover:text-bt-amber transition-colors">
              <PlusCircle className="w-6 h-6 text-slate-400 group-hover:text-bt-amber" />
            </div>
            <div>
              <div className="font-bold text-white text-base group-hover:text-bt-amber transition-colors">
                Сформировать новый отряд
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Стартовый баланс: 3000 SP, 2 пилота, техника из RAT
              </p>
            </div>
          </Link>

          {/* Превью существующих отрядов */}
          {forces &&
            forces.map((force) => (
              <div
                key={force.id}
                onClick={() => navigate(`/forces/${force.id}`)}
                className={`bg-bt-card border border-bt-border hover:border-bt-amber/60 rounded-xl p-6 shadow-xl transition-all cursor-pointer flex flex-col justify-between hover:translate-y-[-2px] group relative ${
                  deletingId === force.id ? 'opacity-40 pointer-events-none' : ''
                }`}
              >
                <div>
                  <div className="flex justify-between items-start mb-2 gap-2">
                    <h2 className="font-bold text-lg text-white group-hover:text-bt-amber transition-colors truncate">
                      {force.name}
                    </h2>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className="text-[10px] uppercase font-mono bg-bt-amber/10 border border-bt-amber/30 text-bt-amber px-2 py-0.5 rounded">
                        {force.sponsoring_faction}
                      </span>
                      <button
                        onClick={(e) => handleDelete(e, force.id, force.name)}
                        className="p-1.5 bg-slate-900 hover:bg-red-950 border border-bt-border hover:border-red-500/50 rounded text-slate-400 hover:text-red-400 transition-colors"
                        title="Удалить отряд"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {/* Статистика */}
                  <div className="grid grid-cols-2 gap-2 bg-slate-900/80 p-3 rounded-lg border border-bt-border/50 my-4 text-xs">
                    <div className="flex items-center gap-2">
                      <Coins className="w-4 h-4 text-bt-amber" />
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-bold">Warchest (SP)</span>
                        <span className="font-mono font-bold text-bt-amber">{force.support_points} SP</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <Award className="w-4 h-4 text-bt-green" />
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-bold">Репутация</span>
                        <span className="font-mono font-bold text-white">{force.reputation_score}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-between text-xs text-slate-400 border-t border-bt-border/40 pt-3">
                    <span className="flex items-center gap-1">
                      <Crosshair className="w-3.5 h-3.5 text-slate-500" /> Техники: <strong className="text-slate-200">{force.units?.length || 0}</strong>
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="w-3.5 h-3.5 text-slate-500" /> Пилотов: <strong className="text-slate-200">{force.pilots?.length || 0}</strong>
                    </span>
                  </div>
                </div>

                <div className="mt-5 flex items-center justify-end text-xs font-bold text-bt-amber group-hover:underline gap-1">
                  Открыть терминал <ArrowRight className="w-4 h-4" />
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};