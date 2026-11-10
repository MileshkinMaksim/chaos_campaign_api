import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { pilotsApi } from '../../api/services';
import * as T from '../../types';
import { 
  getGunneryUpgradeCost, 
  getPilotingUpgradeCost, 
  getEdgeUpgradeCost, 
  getNextSPACost 
} from '../../utils/xpCalculator';
import { 
  Award, 
  Zap, 
  Crosshair, 
  Shield, 
  ChevronLeft, 
  Sparkles, 
  PlusCircle, 
  CheckCircle2 
} from 'lucide-react';

const PRESET_ABILITIES = [
  'Sniper',
  'Marksmanship',
  'Jumping Jack',
  'Dodge',
  'Weapon Specialist',
  'Tactical Genius',
];

export const PilotProgressionPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [selectedAbility, setSelectedAbility] = useState('');
  const [customAbility, setCustomAbility] = useState('');

  const { data: pilot, isLoading, error } = useQuery({
    queryKey: ['pilot', id],
    queryFn: () => pilotsApi.getPilot(id!),
    enabled: !!id,
  });

  const upgradeMutation = useMutation({
    mutationFn: (request: T.PilotUpgradeRequest) => pilotsApi.upgradePilot(id!, request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pilot', id] });
      setSelectedAbility('');
      setCustomAbility('');
    },
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bt-bg text-white flex items-center justify-center font-mono">
        <p className="text-bt-amber animate-pulse">Загрузка личного дела мехварриора...</p>
      </div>
    );
  }

  if (error || !pilot) {
    return (
      <div className="min-h-screen bg-bt-bg text-white p-8 flex flex-col items-center justify-center">
        <div className="bg-bt-card border border-bt-red p-6 rounded-lg text-center max-w-md">
          <h2 className="text-lg font-bold text-bt-red mb-2">Пилот не найден</h2>
          <p className="text-sm text-slate-400 mb-4">
            Не удалось загрузить данные пилота или идентификатор указан неверно.
          </p>
          <button
            onClick={() => navigate(-1)}
            className="bg-bt-amber text-slate-950 font-bold px-4 py-2 rounded text-sm hover:bg-amber-600 transition-colors"
          >
            Вернуться назад
          </button>
        </div>
      </div>
    );
  }

  const gunneryCost = getGunneryUpgradeCost(pilot.gunnery);
  const pilotingCost = getPilotingUpgradeCost(pilot.piloting);
  const edgeCost = getEdgeUpgradeCost(pilot.edge_points);
  const spaCost = getNextSPACost(pilot.special_abilities?.length || 0);

  const handleAbilityUpgrade = (e: React.FormEvent) => {
    e.preventDefault();
    const abilityName = customAbility.trim() || selectedAbility;
    if (!abilityName || !spaCost || pilot.experience_points < spaCost) return;

    upgradeMutation.mutate({
      upgrade_type: 'ability',
      ability_name: abilityName,
    });
  };

  return (
    <div className="min-h-screen bg-bt-bg text-white flex flex-col items-center p-6">
      <div className="w-full max-w-5xl space-y-6">
        {/* Шапка */}
        <div className="flex justify-between items-center border-b border-bt-border pb-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate(pilot.force_id ? `/forces/${pilot.force_id}` : '/')}
              className="p-2 bg-slate-900 border border-bt-border rounded text-slate-400 hover:text-white hover:border-bt-amber transition-colors"
              title="Назад в терминал отряда"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-2xl font-bold tracking-wider uppercase text-white">
                {pilot.name}
              </h1>
              <p className="text-xs text-slate-400 font-mono">
                Терминал повышения квалификации пилота
              </p>
            </div>
          </div>

          {/* Баланс XP */}
          <div className="flex items-center gap-3">
            <div className="bg-slate-900 border border-bt-amber/40 px-4 py-2 rounded-lg flex items-center gap-2">
              <Zap className="w-5 h-5 text-bt-amber animate-pulse" />
              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400 block">
                  Доступный XP
                </span>
                <span className="text-lg font-mono font-bold text-bt-amber">
                  {pilot.experience_points} XP
                </span>
              </div>
            </div>

            <div className="bg-slate-900 border border-bt-border px-4 py-2 rounded-lg flex items-center gap-2">
              <Award className="w-5 h-5 text-bt-green" />
              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400 block">
                  Всего заработано
                </span>
                <span className="text-lg font-mono font-bold text-white">
                  {pilot.total_xp_earned} XP
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Сетка навыков */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Gunnery */}
          <div className="bg-bt-card border border-bt-border rounded-xl p-5 shadow-lg flex flex-col justify-between space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-bold text-slate-400 uppercase flex items-center gap-1.5">
                  <Crosshair className="w-4 h-4 text-bt-amber" /> Gunnery Skill
                </span>
                <span className="text-2xl font-mono font-bold text-white">{pilot.gunnery}</span>
              </div>
              <p className="text-xs text-slate-400">
                Точность стрельбы (меньшее значение улучшает попадание).
              </p>
            </div>

            <div className="border-t border-bt-border/60 pt-4">
              {gunneryCost !== null ? (
                <button
                  disabled={pilot.experience_points < gunneryCost || upgradeMutation.isPending}
                  onClick={() => upgradeMutation.mutate({ upgrade_type: 'gunnery' })}
                  className="w-full py-2 px-3 bg-bt-amber/20 hover:bg-bt-amber border border-bt-amber/50 hover:border-bt-amber text-bt-amber hover:text-slate-950 font-bold text-xs rounded transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5"
                >
                  <Sparkles className="w-4 h-4" /> Улучшить до {pilot.gunnery - 1} ({gunneryCost} XP)
                </button>
              ) : (
                <span className="block text-center text-xs text-bt-green font-bold bg-slate-900/60 py-2 rounded border border-bt-green/30">
                  Максимальный уровень
                </span>
              )}
            </div>
          </div>

          {/* Card 2: Piloting */}
          <div className="bg-bt-card border border-bt-border rounded-xl p-5 shadow-lg flex flex-col justify-between space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-bold text-slate-400 uppercase flex items-center gap-1.5">
                  <Shield className="w-4 h-4 text-bt-amber" /> Piloting Skill
                </span>
                <span className="text-2xl font-mono font-bold text-white">{pilot.piloting}</span>
              </div>
              <p className="text-xs text-slate-400">
                Мастерство пилотирования и удержание равновесия меха.
              </p>
            </div>

            <div className="border-t border-bt-border/60 pt-4">
              {pilotingCost !== null ? (
                <button
                  disabled={pilot.experience_points < pilotingCost || upgradeMutation.isPending}
                  onClick={() => upgradeMutation.mutate({ upgrade_type: 'piloting' })}
                  className="w-full py-2 px-3 bg-bt-amber/20 hover:bg-bt-amber border border-bt-amber/50 hover:border-bt-amber text-bt-amber hover:text-slate-950 font-bold text-xs rounded transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5"
                >
                  <Sparkles className="w-4 h-4" /> Улучшить до {pilot.piloting - 1} ({pilotingCost} XP)
                </button>
              ) : (
                <span className="block text-center text-xs text-bt-green font-bold bg-slate-900/60 py-2 rounded border border-bt-green/30">
                  Максимальный уровень
                </span>
              )}
            </div>
          </div>

          {/* Card 3: Edge */}
          <div className="bg-bt-card border border-bt-border rounded-xl p-5 shadow-lg flex flex-col justify-between space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-bold text-slate-400 uppercase flex items-center gap-1.5">
                  <Zap className="w-4 h-4 text-bt-amber" /> Edge Points
                </span>
                <span className="text-2xl font-mono font-bold text-bt-amber">{pilot.edge_points}</span>
              </div>
              <p className="text-xs text-slate-400">
                Очки переброса критических ситуаций во время боя.
              </p>
            </div>

            <div className="border-t border-bt-border/60 pt-4">
              {edgeCost !== null ? (
                <button
                  disabled={pilot.experience_points < edgeCost || upgradeMutation.isPending}
                  onClick={() => upgradeMutation.mutate({ upgrade_type: 'edge' })}
                  className="w-full py-2 px-3 bg-bt-amber/20 hover:bg-bt-amber border border-bt-amber/50 hover:border-bt-amber text-bt-amber hover:text-slate-950 font-bold text-xs rounded transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-1.5"
                >
                  <Sparkles className="w-4 h-4" /> Увеличить Edge до {pilot.edge_points + 1} ({edgeCost} XP)
                </button>
              ) : (
                <span className="block text-center text-xs text-bt-green font-bold bg-slate-900/60 py-2 rounded border border-bt-green/30">
                  Максимальный уровень
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Секция специальных способностей (SPA) */}
        <div className="bg-bt-card border border-bt-border rounded-xl p-6 shadow-xl space-y-6">
          <div className="flex justify-between items-center border-b border-bt-border/60 pb-3">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-bt-amber" /> Специальные Способности (SPA)
              </h2>
              <p className="text-xs text-slate-400">
                Уникальные боевые навыки мехварриора (максимум 5 способностей).
              </p>
            </div>
            <span className="text-xs font-mono font-bold text-bt-amber bg-slate-900 px-3 py-1 rounded border border-bt-border">
              {pilot.special_abilities?.length || 0} / 5 SPA
            </span>
          </div>

          {/* Список изученных SPA */}
          <div className="space-y-2">
            <span className="text-xs font-bold uppercase text-slate-400 block">
              Изученные навыки:
            </span>
            {pilot.special_abilities && pilot.special_abilities.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {pilot.special_abilities.map((ability, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-1.5 bg-slate-900 border border-bt-amber/40 text-bt-amber font-mono text-xs font-bold px-3 py-1.5 rounded-lg"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-bt-green" /> {ability}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">
                У пилота пока нет изученных специальных способностей.
              </p>
            )}
          </div>

          {/* Форма изучения новой SPA */}
          {spaCost !== null ? (
            <form onSubmit={handleAbilityUpgrade} className="pt-4 border-t border-bt-border/60 space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold uppercase text-slate-300">
                  Изучить новую способность:
                </span>
                <span className="text-xs font-mono font-bold text-bt-amber">
                  Стоимость: {spaCost} XP
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Выбор из готовых пресетов */}
                <div>
                  <label className="block text-[10px] uppercase font-bold text-slate-400 mb-1">
                    Выберите из списка
                  </label>
                  <select
                    value={selectedAbility}
                    onChange={(e) => {
                      setSelectedAbility(e.target.value);
                      setCustomAbility('');
                    }}
                    className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-bt-amber"
                  >
                    <option value="">-- Выберите способность --</option>
                    {PRESET_ABILITIES.filter(
                      (a) => !pilot.special_abilities?.includes(a)
                    ).map((ability) => (
                      <option key={ability} value={ability}>
                        {ability}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Свой вариант названия */}
                <div>
                  <label className="block text-[10px] uppercase font-bold text-slate-400 mb-1">
                    Или введите кастомное название
                  </label>
                  <input
                    type="text"
                    placeholder="Например: Eagle Eye"
                    value={customAbility}
                    onChange={(e) => {
                      setCustomAbility(e.target.value);
                      setSelectedAbility('');
                    }}
                    className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-bt-amber"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={
                  (!selectedAbility && !customAbility.trim()) ||
                  pilot.experience_points < spaCost ||
                  upgradeMutation.isPending
                }
                className="w-full py-2.5 bg-bt-amber hover:bg-amber-500 text-slate-950 font-bold text-xs rounded-lg transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <PlusCircle className="w-4 h-4" /> Изучить способность ({spaCost} XP)
              </button>
            </form>
          ) : (
            <div className="p-3 bg-slate-900 border border-bt-border text-center text-xs text-slate-400 rounded">
              Достигнут лимит в 5 специальных способностей.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};