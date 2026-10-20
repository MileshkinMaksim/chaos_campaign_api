import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { forcesApi } from '../../api/services';
import type { StartingFactionOption, StartingMechSelection } from '../../types';
import { Faction } from '../../types';
import { Shield, Users, Crosshair, AlertTriangle, CheckCircle, ChevronRight, ChevronLeft } from 'lucide-react';

export const ForceCreationPage: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Опции с сервера
  const [factionOptions, setFactionOptions] = useState<StartingFactionOption[]>([]);
  const [maxBV2, setMaxBV2] = useState(3000);

  // Форма отряда
  const [forceName, setForceName] = useState('');
  const [selectedFaction, setSelectedFaction] = useState<Faction>(Faction.MERCENARY);
  const [pilot1, setPilot1] = useState('Pilot Alpha');
  const [pilot2, setPilot2] = useState('Pilot Bravo');
  const [selectedMechs, setSelectedMechs] = useState<StartingMechSelection[]>([]);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const data = await forcesApi.getStartingOptions();
        if (data.available_factions && data.available_factions.length > 0) {
          setFactionOptions(data.available_factions);
          setSelectedFaction(data.available_factions[0].faction);
        }
        if (data.max_starting_bv2) setMaxBV2(data.max_starting_bv2);
      } catch (err: any) {
        // Фоллбек-данные для разработки
        setFactionOptions([
          {
            faction: Faction.MERCENARY,
            display_name: 'Mercenary',
            description: 'Наемные подразделения',
            available_rat_mechs: [
              { chassis: 'Locust', model: 'LCT-1V', tonnage: 20, weight_class: 'Light' as any, bv2: 532 },
              { chassis: 'Commando', model: 'COM-2D', tonnage: 25, weight_class: 'Light' as any, bv2: 541 },
              { chassis: 'Centurion', model: 'CN9-A', tonnage: 50, weight_class: 'Medium' as any, bv2: 945 },
              { chassis: 'Shadow Hawk', model: 'SHD-2H', tonnage: 55, weight_class: 'Medium' as any, bv2: 1064 },
              { chassis: 'Warhammer', model: 'WHM-6R', tonnage: 70, weight_class: 'Heavy' as any, bv2: 1299 }
            ]
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOptions();
  }, []);

  const activeFactionObj = factionOptions.find((f) => f.faction === selectedFaction) || factionOptions[0];
  const availableRatMechs = activeFactionObj?.available_rat_mechs || [];

  const totalBV2 = selectedMechs.reduce((sum, mech) => sum + mech.bv2, 0);
  const isBV2Exceeded = totalBV2 > maxBV2;
  const isMechCountExceeded = selectedMechs.length > 2;

  const toggleMechSelection = (mech: StartingMechSelection) => {
    const exists = selectedMechs.some((m) => m.model === mech.model && m.chassis === mech.chassis);
    if (exists) {
      setSelectedMechs(selectedMechs.filter((m) => !(m.model === mech.model && m.chassis === mech.chassis)));
    } else {
      if (selectedMechs.length >= 2) return;
      setSelectedMechs([...selectedMechs, mech]);
    }
  };

  const handleSubmit = async () => {
    if (isBV2Exceeded || isMechCountExceeded || selectedMechs.length === 0) return;
    setError(null);
    setIsSubmitting(true);

    try {
      const newForce = await forcesApi.createForce({
        name: forceName,
        sponsoring_faction: selectedFaction,
        starting_pilot_names: [pilot1, pilot2],
        selected_mechs: selectedMechs,
      });
      navigate(`/forces/${newForce.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось сформировать отряд');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-bt-bg text-white flex items-center justify-center">
        <p className="text-bt-amber animate-pulse font-mono">Загрузка стартовых параметров v0.2...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bt-bg text-white p-6 flex flex-col items-center">
      <div className="w-full max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-bt-amber tracking-wider uppercase mb-2">
            Мастер формирования наемного отряда
          </h1>
          <p className="text-slate-400 text-sm">Шаг {step} из 4</p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-900/50 border border-bt-red rounded text-red-200 text-sm flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="bg-bt-card border border-bt-border rounded-lg p-6 shadow-2xl">
          {/* Шаг 1: Название и Фракция */}
          {step === 1 && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-bt-border pb-2">
                <Shield className="text-bt-amber" /> Шаг 1: Название отряда и Фракция
              </h2>
              <div>
                <label className="block text-xs uppercase font-bold text-slate-400 mb-2">
                  Название подразделения (3-50 символов)
                </label>
                <input
                  type="text"
                  value={forceName}
                  onChange={(e) => setForceName(e.target.value)}
                  placeholder="например: 2nd Iron Hounds"
                  className="w-full bg-slate-900 border border-bt-border rounded p-3 text-white focus:outline-none focus:border-bt-amber"
                />
              </div>

              <div>
                <label className="block text-xs uppercase font-bold text-slate-400 mb-2">
                  Фракция происхождения
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {factionOptions.map((opt) => (
                    <button
                      key={opt.faction}
                      type="button"
                      onClick={() => {
                        setSelectedFaction(opt.faction);
                        setSelectedMechs([]);
                      }}
                      className={`p-3 rounded border text-left font-medium transition-colors ${
                        selectedFaction === opt.faction
                          ? 'bg-bt-amber/20 border-bt-amber text-bt-amber'
                          : 'bg-slate-900 border-bt-border text-slate-300 hover:border-slate-500'
                      }`}
                    >
                      <div className="font-bold">{opt.display_name || opt.faction}</div>
                      {opt.description && <div className="text-xs text-slate-400 mt-1">{opt.description}</div>}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Шаг 2: Имена пилотов */}
          {step === 2 && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-bt-border pb-2">
                <Users className="text-bt-amber" /> Шаг 2: Стартовые мехварриоры
              </h2>
              <p className="text-xs text-bt-amber bg-bt-amber/10 p-3 rounded border border-bt-amber/30">
                Каждый пилот получает 150 XP на старте для последующего развития навыков.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs uppercase font-bold text-slate-400 mb-2">
                    Позывной пилота 1
                  </label>
                  <input
                    type="text"
                    value={pilot1}
                    onChange={(e) => setPilot1(e.target.value)}
                    className="w-full bg-slate-900 border border-bt-border rounded p-3 text-white focus:outline-none focus:border-bt-amber"
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase font-bold text-slate-400 mb-2">
                    Позывной пилота 2
                  </label>
                  <input
                    type="text"
                    value={pilot2}
                    onChange={(e) => setPilot2(e.target.value)}
                    className="w-full bg-slate-900 border border-bt-border rounded p-3 text-white focus:outline-none focus:border-bt-amber"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Шаг 3: Техника из RAT */}
          {step === 3 && (
            <div className="space-y-6">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-bt-border pb-2 gap-2">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                  <Crosshair className="text-bt-amber" /> Шаг 3: Выбор техники из RAT (до 2 мехов)
                </h2>
                <div className="flex gap-4 font-mono text-sm">
                  <span className={selectedMechs.length > 2 ? 'text-bt-red font-bold' : 'text-slate-300'}>
                    Выбрано: {selectedMechs.length} / 2
                  </span>
                  <span className={isBV2Exceeded ? 'text-bt-red font-bold' : 'text-bt-green'}>
                    Суммарный BV2: {totalBV2} / {maxBV2}
                  </span>
                </div>
              </div>

              {isBV2Exceeded && (
                <div className="p-3 bg-red-900/40 border border-bt-red text-red-200 text-xs rounded">
                  Превышен лимит BV2! Сумма не должна превышать {maxBV2} BV2.
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto pr-2">
                {availableRatMechs.map((mech) => {
                  const isSelected = selectedMechs.some((m) => m.model === mech.model && m.chassis === mech.chassis);
                  return (
                    <div
                      key={`${mech.chassis}-${mech.model}`}
                      onClick={() => toggleMechSelection(mech)}
                      className={`p-4 rounded border cursor-pointer transition-all ${
                        isSelected
                          ? 'bg-bt-amber/20 border-bt-amber'
                          : 'bg-slate-900 border-bt-border hover:border-slate-500'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-bold text-white">{mech.chassis} {mech.model}</span>
                        <span className="text-xs bg-slate-800 text-bt-amber px-2 py-1 rounded font-mono">
                          {mech.bv2} BV2
                        </span>
                      </div>
                      <div className="text-xs text-slate-400 flex justify-between">
                        <span>Класс: {mech.weight_class}</span>
                        <span>Тоннаж: {mech.tonnage} т</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Шаг 4: Сводка */}
          {step === 4 && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-bt-border pb-2">
                <CheckCircle className="text-bt-green" /> Шаг 4: Итоговая сводка
              </h2>

              <div className="grid grid-cols-2 gap-4 bg-slate-900 p-4 rounded border border-bt-border text-sm">
                <div>
                  <span className="text-slate-400 block text-xs uppercase">Название:</span>
                  <span className="font-bold text-white">{forceName}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-xs uppercase">Фракция:</span>
                  <span className="font-bold text-bt-amber">{selectedFaction}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-xs uppercase">Стартовый баланс:</span>
                  <span className="font-bold text-bt-green">3000 SP</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-xs uppercase">Репутация:</span>
                  <span className="font-bold text-white">1</span>
                </div>
              </div>

              <div>
                <h3 className="text-xs uppercase font-bold text-slate-400 mb-2">Пилоты:</h3>
                <div className="flex gap-4">
                  <span className="bg-slate-900 border border-bt-border px-3 py-1 rounded text-sm text-slate-200">
                    {pilot1} (150 XP)
                  </span>
                  <span className="bg-slate-900 border border-bt-border px-3 py-1 rounded text-sm text-slate-200">
                    {pilot2} (150 XP)
                  </span>
                </div>
              </div>

              <div>
                <h3 className="text-xs uppercase font-bold text-slate-400 mb-2">Выбранная техника:</h3>
                <div className="grid grid-cols-2 gap-3">
                  {selectedMechs.map((m) => (
                    <div key={`${m.chassis}-${m.model}`} className="bg-slate-900 p-3 rounded border border-bt-border text-xs">
                      <div className="font-bold text-white">{m.chassis} {m.model}</div>
                      <div className="text-slate-400">{m.bv2} BV2 | {m.tonnage} т</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Панель навигации */}
          <div className="mt-8 flex justify-between items-center pt-4 border-t border-bt-border">
            {step > 1 ? (
              <button
                type="button"
                onClick={() => setStep(step - 1)}
                className="flex items-center gap-1 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold px-4 py-2 rounded transition-colors text-sm"
              >
                <ChevronLeft className="w-4 h-4" /> Назад
              </button>
            ) : (
              <div />
            )}

            {step < 4 ? (
              <button
                type="button"
                disabled={
                  (step === 1 && forceName.trim().length < 3) ||
                  (step === 2 && (!pilot1.trim() || !pilot2.trim())) ||
                  (step === 3 && (selectedMechs.length === 0 || isBV2Exceeded))
                }
                onClick={() => setStep(step + 1)}
                className="flex items-center gap-1 bg-bt-amber hover:bg-amber-600 text-slate-950 font-bold px-4 py-2 rounded transition-colors text-sm disabled:opacity-50"
              >
                Далее <ChevronRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                disabled={isSubmitting}
                onClick={handleSubmit}
                className="bg-bt-green hover:bg-emerald-600 text-slate-950 font-bold px-6 py-2 rounded transition-colors text-sm disabled:opacity-50"
              >
                {isSubmitting ? 'Формирование...' : 'Сформировать отряд'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};