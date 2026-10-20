import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { forcesApi } from '../../api/services';
import { MechStatusBadge } from '../../components/domain/MechStatusBadge';
import { useAuthStore } from '../../store/authStore';
import { 
  Shield, 
  Coins, 
  Award, 
  Download, 
  Users, 
  Crosshair, 
  UserCheck, 
  LogOut,
  ChevronRight,
  ChevronLeft
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const logout = useAuthStore((state) => state.logout);
  const [activeTab, setActiveTab] = useState<'mechs' | 'pilots'>('mechs');

  // Загрузка данных отряда с использованием TanStack Query
  const { data: force, isLoading, error } = useQuery({
    queryKey: ['force', id],
    queryFn: () => forcesApi.getForce(id!),
    enabled: !!id,
  });

  // Мутация назначения пилота на мех
  const assignPilotMutation = useMutation({
    mutationFn: (payload: { unit_id: string; pilot_id?: string | null }) =>
      forcesApi.assignPilot(id!, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['force', id] });
    },
  });

  // Скачивание Force Record Sheet
  const handleExportSheet = async () => {
  if (!id || !force) return;
  try {
    const rawData = await forcesApi.exportRecordSheet(id);
    
    let blob: Blob;
    if (rawData instanceof Blob) {
      blob = rawData;
    } else if (rawData && (rawData as any).data instanceof Blob) {
      blob = (rawData as any).data;
    } else {
      blob = new Blob([JSON.stringify(rawData)], { type: 'application/json' });
    }

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${force.name}_record_sheet.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Даем браузеру время зарегистрировать событие скачивания
    setTimeout(() => {
      window.URL.revokeObjectURL(url);
    }, 1000);
  } catch (err) {
    console.error('Ошибка при экспорте Record Sheet', err);
  }
};

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bt-bg text-white flex items-center justify-center font-mono">
        <p className="text-bt-amber animate-pulse">Загрузка данных командного терминала...</p>
      </div>
    );
  }

  if (error || !force) {
    return (
      <div className="min-h-screen bg-bt-bg text-white p-8 flex flex-col items-center justify-center">
        <div className="bg-bt-card border border-bt-red p-6 rounded-lg text-center max-w-md">
          <h2 className="text-lg font-bold text-bt-red mb-2">Отряд не найден</h2>
          <p className="text-sm text-slate-400 mb-4">
            Не удалось загрузить структуру отряда или у вас нет прав доступа.
          </p>
          <Link
            to="/"
            className="inline-block bg-bt-amber text-slate-950 font-bold px-4 py-2 rounded text-sm hover:bg-amber-600 transition-colors"
          >
            Вернуться в штаб
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bt-bg text-white flex flex-col">
      {/* Верхняя навигационная панель */}
      <header className="bg-bt-card border-b border-bt-border px-6 py-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex items-center gap-3">
          <Link
            to="/"
            className="p-2 bg-slate-900 border border-bt-border rounded text-slate-400 hover:text-white hover:border-bt-amber transition-colors"
            title="К списку всех отрядов"
          >
            <ChevronLeft className="w-5 h-5" />
          </Link>
          <Shield className="w-8 h-8 text-bt-amber flex-shrink-0" />
          <div>
            <h1 className="text-xl font-bold tracking-wide text-white">{force.name}</h1>
            <p className="text-xs text-bt-amber uppercase font-mono">{force.sponsoring_faction}</p>
          </div>
        </div>

        {/* Быстрая статистика баланса и репутации */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="bg-slate-900 border border-bt-border px-4 py-2 rounded flex items-center gap-2">
            <Coins className="w-5 h-5 text-bt-amber" />
            <div>
              <div className="text-[10px] uppercase font-bold text-slate-400">Warchest Balance</div>
              <div className="text-sm font-mono font-bold text-bt-amber">{force.support_points} SP</div>
            </div>
          </div>

          <div className="bg-slate-900 border border-bt-border px-4 py-2 rounded flex items-center gap-2">
            <Award className="w-5 h-5 text-bt-green" />
            <div>
              <div className="text-[10px] uppercase font-bold text-slate-400">Reputation Score</div>
              <div className="text-sm font-mono font-bold text-white">{force.reputation_score}</div>
            </div>
          </div>

          <button
            onClick={handleExportSheet}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 border border-bt-border text-slate-200 font-bold px-3 py-2 rounded text-xs transition-colors"
            title="Скачать Mercenary Force Record Sheet"
          >
            <Download className="w-4 h-4 text-bt-amber" /> Record Sheet
          </button>

          <button
            onClick={logout}
            className="flex items-center gap-1 bg-red-950/60 hover:bg-red-900 border border-bt-red/40 text-red-300 font-bold px-3 py-2 rounded text-xs transition-colors"
            title="Выход из терминала"
          >
            <LogOut className="w-4 h-4" /> Выход
          </button>
        </div>
      </header>

      {/* Быстрое меню навигации по разделам */}
      <nav className="bg-slate-900/60 border-b border-bt-border px-6 py-2 flex gap-4 text-xs font-bold uppercase tracking-wider overflow-x-auto">
        <span className="text-bt-amber border-b-2 border-bt-amber pb-1 cursor-default">Обзор отряда</span>
        <Link to="/pilots" className="text-slate-400 hover:text-white transition-colors pb-1">Прокачка пилотов</Link>
        <Link to="/contracts" className="text-slate-400 hover:text-white transition-colors pb-1">Контракты</Link>
        <Link to="/tracks" className="text-slate-400 hover:text-white transition-colors pb-1">Миссии</Link>
        <Link to="/logistics" className="text-slate-400 hover:text-white transition-colors pb-1">Логистика</Link>
      </nav>

      {/* Основной контент Дашборда */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* Переключатель вкладок Дашборда */}
        <div className="flex border-b border-bt-border">
          <button
            onClick={() => setActiveTab('mechs')}
            className={`flex items-center gap-2 px-6 py-3 font-bold text-sm border-b-2 transition-colors ${
              activeTab === 'mechs'
                ? 'border-bt-amber text-bt-amber bg-slate-800/40'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Crosshair className="w-4 h-4" /> Ангар техники ({force.units.length})
          </button>
          <button
            onClick={() => setActiveTab('pilots')}
            className={`flex items-center gap-2 px-6 py-3 font-bold text-sm border-b-2 transition-colors ${
              activeTab === 'pilots'
                ? 'border-bt-amber text-bt-amber bg-slate-800/40'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Users className="w-4 h-4" /> Ростер мехвоинов ({force.pilots.length})
          </button>
        </div>

        {/* Вкладка 1: Ангар техники */}
        {activeTab === 'mechs' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {force.units.map((unit) => {
                return (
                  <div
                    key={unit.id}
                    className="bg-bt-card border border-bt-border rounded-lg p-5 shadow-lg flex flex-col justify-between space-y-4"
                  >
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="font-bold text-white text-lg">{unit.chassis}</h3>
                          <p className="text-xs font-mono text-slate-400">{unit.model}</p>
                        </div>
                        <MechStatusBadge status={unit.status} />
                      </div>

                      <div className="grid grid-cols-3 gap-2 bg-slate-900/80 p-2.5 rounded text-xs text-center border border-bt-border/50 my-3">
                        <div>
                          <span className="text-slate-500 block text-[10px] uppercase">Класс</span>
                          <span className="font-semibold text-slate-200">{unit.weight_class}</span>
                        </div>
                        <div>
                          <span className="text-slate-500 block text-[10px] uppercase">Тоннаж</span>
                          <span className="font-semibold text-slate-200">{unit.tonnage} т</span>
                        </div>
                        <div>
                          <span className="text-slate-500 block text-[10px] uppercase">BV2</span>
                          <span className="font-semibold text-bt-amber font-mono">{unit.bv2}</span>
                        </div>
                      </div>
                    </div>

                    {/* Назначение пилота */}
                    <div className="pt-3 border-t border-bt-border/60">
                      <label className="block text-[10px] uppercase font-bold text-slate-400 mb-1 flex items-center gap-1">
                        <UserCheck className="w-3.5 h-3.5 text-bt-amber" /> Назначенный пилот
                      </label>
                      <select
                        value={unit.assigned_pilot_id || ''}
                        disabled={assignPilotMutation.isPending}
                        onChange={(e) =>
                          assignPilotMutation.mutate({
                            unit_id: unit.id,
                            pilot_id: e.target.value || null,
                          })
                        }
                        className="w-full bg-slate-900 border border-bt-border rounded px-3 py-1.5 text-xs text-white focus:outline-none focus:border-bt-amber"
                      >
                        <option value="">-- Без пилота --</option>
                        {force.pilots.map((p) => (
                          <option key={p.id} value={p.id}>
                            {p.name} (Gunnery {p.gunnery} / Piloting {p.piloting})
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Вкладка 2: Ростер мехвоинов */}
        {activeTab === 'pilots' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {force.pilots.map((pilot) => {
              const assignedUnit = force.units.find((u) => u.assigned_pilot_id === pilot.id);

              return (
                <div
                  key={pilot.id}
                  className="bg-bt-card border border-bt-border rounded-lg p-5 shadow-lg space-y-4"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-white text-lg">{pilot.name}</h3>
                      <p className="text-xs text-slate-400">
                        Прикрепленный мех:{' '}
                        {assignedUnit ? (
                          <span className="text-bt-amber font-medium">
                            {assignedUnit.chassis} {assignedUnit.model}
                          </span>
                        ) : (
                          <span className="text-slate-500 italic">Не назначен</span>
                        )}
                      </p>
                    </div>
                    <span className="bg-bt-amber/20 border border-bt-amber/40 text-bt-amber font-mono font-bold text-xs px-2.5 py-1 rounded">
                      {pilot.experience_points} XP
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 bg-slate-900/80 p-3 rounded text-center border border-bt-border/50">
                    <div>
                      <span className="text-slate-500 block text-[10px] uppercase font-bold">Gunnery</span>
                      <span className="text-base font-bold text-white">{pilot.gunnery}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px] uppercase font-bold">Piloting</span>
                      <span className="text-base font-bold text-white">{pilot.piloting}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block text-[10px] uppercase font-bold">Edge</span>
                      <span className="text-base font-bold text-bt-amber">{pilot.edge_points}</span>
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-2">
                    <span className="text-xs text-slate-400">
                      Всего заработано XP: <span className="font-mono text-slate-200">{pilot.total_xp_earned}</span>
                    </span>
                    <Link
                      to={`/pilots/${pilot.id}`}
                      className="inline-flex items-center gap-1 text-xs font-bold text-bt-amber hover:underline"
                    >
                      Прокачка <ChevronRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
};