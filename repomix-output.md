This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: cmake-build-*/**, **/TestData/**, **/*.txt, **/*.lock, **/package-lock.json, **/pnpm-lock.yaml, **/yarn.lock, **/dist/**, **/build/**, **/coverage/**, **/*.min.*, **/*.map, **/*.svg, **/*.png, **/*.jpg, **/*.pdf, **/*.sqlite, **/*.db, **/*.log, **/CMakeLists.txt, **/Autotest_Data/**, **/benchmark/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
````
app/
  api/
    v1/
      endpoints/
        __init__.py
        auth.py
        contracts.py
        forces.py
        generator.py
        logistics.py
        pilots.py
        tracks.py
      __init__.py
      api.py
    __init__.py
  core/
    __init__.py
    exceptions.py
    security.py
  db/
    models/
      __init__.py
      force.py
      pilot.py
      user.py
    __init__.py
    database.py
  dependencies/
    __init__.py
    auth.py
    campaign.py
    db.py
  schemas/
    __init__.py
    auth.py
    contract.py
    force.py
    generator.py
    logistics.py
    pilot.py
    track.py
  services/
    __init__.py
    force_service.py
    generator_service.py
    logistics_service.py
    negotiation_engine.py
    pilot_service.py
    track_service.py
  tests/
    __init__.py
    conftest.py
    test_force.py
    test_negotiation.py
    test_pilots.py
    test_tracks.py
  __init__.py
  config.py
  main.py
frontend/
  src/
    api/
      client.ts
      services.ts
    components/
      common/
        ProtectedRoute.tsx
      domain/
        ContractNegotiationModal.tsx
        MechStatusBadge.tsx
    pages/
      Auth/
        LoginPage.tsx
        RegisterPage.tsx
      Contracts/
        ContractsPage.tsx
      Dashboard/
        DashboardPage.tsx
      ForceSelection/
        ForceSelectionPage.tsx
      ForceWizard/
        ForceCreationPage.tsx
      Pilot/
        PilotProgressionPage.tsx
    store/
      authStore.ts
    types/
      auth.ts
      index.ts
    utils/
      xpCalculator.ts
    App.css
    App.tsx
    index.css
    main.tsx
  .oxlintrc.json
  Dockerfile
  index.html
  nginx.conf
  package.json
  postcss.config.js
  tailwind.config.js
  tsconfig.app.json
  tsconfig.json
  tsconfig.node.json
  vite.config.ts
src/
  chaos_campaign_api/
    __init__.py
.dockerignore
.gitignore
.python-version
docker-compose.yml
Dockerfile
pyproject.toml
pytest.ini
README.md
repomix-output.xml
````

# Files

## File: frontend/src/components/domain/ContractNegotiationModal.tsx
````typescript
import React, { useState } from 'react';
import {
  CommandRights, 
  SalvageRights 
} from '../../api/services';
import { X, Handshake, AlertTriangle, ShieldCheck } from 'lucide-react';
import type { ContractResponse, ContractTerms } from '../../api/services';

interface ContractNegotiationModalProps {
  contract: ContractResponse;
  userReputation: number;
  isOpen: boolean;
  onClose: () => void;
  onNegotiate: (terms: ContractTerms) => Promise<void>;
  isPending: boolean;
}

export const ContractNegotiationModal: React.FC<ContractNegotiationModalProps> = ({
  contract,
  userReputation,
  isOpen,
  onClose,
  onNegotiate,
  isPending,
}) => {
  const [terms, setTerms] = useState<ContractTerms>({ ...contract.terms });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    try {
      await onNegotiate(terms);
      onClose();
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Не удалось согласовать новые условия контракта';
      setErrorMessage(msg);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-bt-card border border-bt-border rounded-lg max-w-xl w-full p-6 space-y-6 shadow-2xl">
        {/* Заголовок */}
        <div className="flex justify-between items-center border-b border-bt-border pb-4">
          <div className="flex items-center gap-2">
            <Handshake className="w-6 h-6 text-bt-amber" />
            <h2 className="text-lg font-bold text-white">Переговоры: {contract.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Текущая репутация отряда */}
        <div className="bg-slate-900 p-3 rounded border border-bt-border/60 flex items-center justify-between text-xs font-mono">
          <span className="text-slate-400">Репутация вашего отряда:</span>
          <span className="text-bt-green font-bold flex items-center gap-1">
            <ShieldCheck className="w-4 h-4" /> {userReputation} pts
          </span>
        </div>

        {errorMessage && (
          <div className="bg-red-950/60 border border-bt-red/60 text-red-300 p-3 rounded text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-bt-red" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            {/* Базовая выплата (SP) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Базовая выплата (SP)
              </label>
              <input
                type="number"
                step="50"
                min="0"
                value={terms.base_payment_sp}
                onChange={(e) => setTerms({ ...terms, base_payment_sp: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>

            {/* Накладные расходы (SP) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Накладные расходы (SP)
              </label>
              <input
                type="number"
                step="50"
                min="0"
                value={terms.overhead_sp}
                onChange={(e) => setTerms({ ...terms, overhead_sp: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>

            {/* Права на командование */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Командование
              </label>
              <select
                value={terms.command_rights}
                onChange={(e) => setTerms({ ...terms, command_rights: e.target.value as CommandRights })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-bt-amber"
              >
                <option value={CommandRights.INDEPENDENT}>Independent (Независимое)</option>
                <option value={CommandRights.CO_COMMAND}>Co-Command (Совместное)</option>
                <option value={CommandRights.INTEGRATED}>Integrated (Подчинение)</option>
              </select>
            </div>

            {/* Права на трофеи */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Права на трофеи (Salvage)
              </label>
              <select
                value={terms.salvage_rights}
                onChange={(e) => setTerms({ ...terms, salvage_rights: e.target.value as SalvageRights })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-bt-amber"
              >
                <option value={SalvageRights.FULL}>Full (Полный трофей)</option>
                <option value={SalvageRights.SHARED}>Shared (Разделение)</option>
                <option value={SalvageRights.EXCHANGE}>Exchange (Обмен)</option>
                <option value={SalvageRights.NONE}>None (Без трофеев)</option>
              </select>
            </div>

            {/* Техподдержка (%) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Покрытие ремонта (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={terms.support_rights_percent}
                onChange={(e) => setTerms({ ...terms, support_rights_percent: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>

            {/* Транспорт (%) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Покрытие транспорта (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={terms.transport_coverage_percent}
                onChange={(e) => setTerms({ ...terms, transport_coverage_percent: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-bt-border">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded transition-colors"
            >
              Отмена
            </button>
            <button
              type="submit"
              disabled={isPending}
              className="px-4 py-2 bg-bt-amber hover:bg-amber-600 text-slate-950 font-bold text-xs rounded transition-colors disabled:opacity-50"
            >
              {isPending ? 'Согласование...' : 'Предложить условия'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
````

## File: frontend/src/pages/Contracts/ContractsPage.tsx
````typescript
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { contractsApi} from '../../api/services';
import type { ContractResponse, ContractTerms } from '../../api/services';
import { forcesApi } from '../../api/services';
import { ContractNegotiationModal } from '../../components/domain/ContractNegotiationModal';
import { 
  FileText,
  Lock, 
  CheckCircle2, 
  PlusCircle, 
  ChevronLeft,
  Filter, 
  Handshake, 
  PenTool 
} from 'lucide-react';

export const ContractsPage: React.FC = () => {
  const { forceId } = useParams<{ forceId?: string }>();
  const queryClient = useQueryClient();
  const [selectedEmployer, setSelectedEmployer] = useState<string>('');
  const [negotiatingContract, setNegotiatingContract] = useState<ContractResponse | null>(null);

  // Загрузка активного отряда
  const { data: force } = useQuery({
    queryKey: ['force', forceId],
    queryFn: () => forcesApi.getForce(forceId!),
    enabled: !!forceId,
  });

  // Загрузка доступных контрактов
  const { data: contracts = [], isLoading, refetch } = useQuery({
    queryKey: ['contracts', selectedEmployer],
    queryFn: () => contractsApi.getAvailableContracts(selectedEmployer ? { employer: selectedEmployer } : undefined),
  });

  // Мутация переговоров
  const negotiateMutation = useMutation({
    mutationFn: ({ contractId, terms }: { contractId: string; terms: ContractTerms }) =>
      contractsApi.negotiateContract(contractId, { requested_terms: terms }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contracts'] });
    },
  });

  // Мутация подписания контракта
  const signMutation = useMutation({
    mutationFn: (contractId: string) => contractsApi.signContract(contractId, forceId!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contracts'] });
      queryClient.invalidateQueries({ queryKey: ['force', forceId] });
      alert('Контракт успешно подписан!');
    },
  });

  // Генерация процедурного контракта
  const generateMutation = useMutation({
    mutationFn: contractsApi.generateContract,
    onSuccess: () => {
      refetch();
    },
  });

  const userReputation = force?.reputation_score || 1;

  return (
    <div className="min-h-screen bg-bt-bg text-white flex flex-col font-sans">
      {/* Шапка навигации */}
      <header className="bg-bt-card border-b border-bt-border px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Link
            to={forceId ? `/forces/${forceId}` : '/'}
            className="p-2 bg-slate-900 border border-bt-border rounded text-slate-400 hover:text-white transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </Link>
          <FileText className="w-8 h-8 text-bt-amber" />
          <div>
            <h1 className="text-xl font-bold uppercase tracking-wide">Доска Контрактов</h1>
            <p className="text-xs text-slate-400">
              Выбор военных заказов в секторе Draconis Reach[cite: 2]
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 border border-bt-border text-bt-amber font-bold px-3 py-2 rounded text-xs transition-colors"
          >
            <PlusCircle className="w-4 h-4" /> Сгенерировать новый заказ
          </button>
        </div>
      </header>

      {/* Панель фильтрации */}
      <div className="bg-slate-900/60 border-b border-bt-border px-6 py-3 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-bt-amber" />
          <span className="text-xs uppercase font-bold text-slate-400">Наниматель:</span>
          <select
            value={selectedEmployer}
            onChange={(e) => setSelectedEmployer(e.target.value)}
            className="bg-slate-900 border border-bt-border rounded px-3 py-1 text-xs text-white focus:outline-none focus:border-bt-amber"
          >
            <option value="">Все фракции</option>
            <option value="Draconis Combine">Draconis Combine</option>
            <option value="Federated Suns">Federated Suns</option>
            <option value="Mercenary">Mercenary Market</option>
          </select>
        </div>

        {force && (
          <div className="text-xs font-mono">
            <span className="text-slate-400">Репутация отряда {force.name}: </span>
            <span className="text-bt-amber font-bold">{force.reputation_score} pts</span>
          </div>
        )}
      </div>

      {/* Список контрактов */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto">
        {isLoading ? (
          <div className="text-center text-bt-amber py-12 font-mono animate-pulse">
            Поиск военных контрактов...
          </div>
        ) : contracts.length === 0 ? (
          <div className="bg-bt-card border border-bt-border p-8 rounded-lg text-center max-w-md mx-auto my-12">
            <p className="text-slate-400 text-sm mb-4">Доступные контракты не найдены.</p>
            <button
              onClick={() => generateMutation.mutate()}
              className="bg-bt-amber text-slate-950 font-bold px-4 py-2 rounded text-xs hover:bg-amber-600 transition-colors"
            >
              Сгенерировать случайный контракт
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {contracts.map((contract) => {
              const meetsReputation = userReputation >= contract.required_reputation;

              return (
                <div
                  key={contract.id}
                  className="bg-bt-card border border-bt-border rounded-lg p-5 flex flex-col justify-between space-y-4 shadow-xl"
                >
                  <div>
                    {/* Заголовок и индикатор репутации */}
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold text-white text-base">{contract.title}</h3>
                        <p className="text-xs font-mono text-bt-amber">{contract.location_hot_spot}</p>
                      </div>
                      {meetsReputation ? (
                        <span className="flex items-center gap-1 text-[10px] bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 font-bold px-2 py-0.5 rounded" title="Репутация подходит">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Доступен
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-[10px] bg-red-950/80 border border-bt-red/40 text-red-300 font-bold px-2 py-0.5 rounded" title="Недостаточно репутации">
                          <Lock className="w-3.5 h-3.5" /> Rep {contract.required_reputation}
                        </span>
                      )}
                    </div>

                    {/* Фракции */}
                    <div className="text-xs text-slate-400 space-y-0.5 my-3 bg-slate-900/60 p-2.5 rounded border border-bt-border/40">
                      <div>
                        <span className="text-slate-500 font-bold uppercase text-[10px]">Наниматель:</span>{' '}
                        <span className="text-slate-200">{contract.employer}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 font-bold uppercase text-[10px]">Противник:</span>{' '}
                        <span className="text-bt-red">{contract.target_faction}</span>
                      </div>
                    </div>

                    {/* Финансовые условия */}
                    <div className="grid grid-cols-2 gap-2 bg-slate-900 p-3 rounded border border-bt-border/50 text-xs text-center font-mono my-3">
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Выплата</span>
                        <span className="text-bt-amber font-bold">{contract.terms.base_payment_sp} SP</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Оверхед</span>
                        <span className="text-white font-bold">{contract.terms.overhead_sp} SP</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Командование</span>
                        <span className="text-slate-300 text-[10px] font-sans">{contract.terms.command_rights}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Трофеи</span>
                        <span className="text-slate-300 text-[10px] font-sans">{contract.terms.salvage_rights}</span>
                      </div>
                    </div>
                  </div>

                  {/* Кнопки действий */}
                  <div className="pt-3 border-t border-bt-border/60 flex items-center gap-2">
                    <button
                      onClick={() => setNegotiatingContract(contract)}
                      className="flex-1 flex items-center justify-center gap-1 bg-slate-800 hover:bg-slate-700 border border-bt-border text-slate-200 font-bold py-2 rounded text-xs transition-colors"
                    >
                      <Handshake className="w-3.5 h-3.5 text-bt-amber" /> Переговоры
                    </button>

                    {forceId && (
                      <button
                        onClick={() => signMutation.mutate(contract.id)}
                        disabled={!meetsReputation || contract.is_signed || signMutation.isPending}
                        className="flex-1 flex items-center justify-center gap-1 bg-bt-amber hover:bg-amber-600 text-slate-950 font-bold py-2 rounded text-xs transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                      >
                        <PenTool className="w-3.5 h-3.5" /> {contract.is_signed ? 'Подписан' : 'Подписать'}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* Модалка переговоров */}
      {negotiatingContract && (
        <ContractNegotiationModal
          contract={negotiatingContract}
          userReputation={userReputation}
          isOpen={!!negotiatingContract}
          onClose={() => setNegotiatingContract(null)}
          isPending={negotiateMutation.isPending}
          onNegotiate={async (terms) => {
            await negotiateMutation.mutateAsync({
              contractId: negotiatingContract.id,
              terms,
            });
          }}
        />
      )}
    </div>
  );
};
````

## File: frontend/src/pages/Pilot/PilotProgressionPage.tsx
````typescript
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
````

## File: frontend/src/utils/xpCalculator.ts
````typescript
export const GUNNERY_UPGRADE_COSTS: Record<number, number> = {
  4: 300,  // 4 -> 3
  3: 700,  // 3 -> 2
  2: 1200, // 2 -> 1
  1: 2200, // 1 -> 0
};

export const PILOTING_UPGRADE_COSTS: Record<number, number> = {
  5: 100,  // 5 -> 4
  4: 200,  // 4 -> 3
  3: 700,  // 3 -> 2
  2: 1200, // 2 -> 1
};

export const EDGE_UPGRADE_COSTS: Record<number, number> = {
  1: 60,   // 1 -> 2
  2: 120,
  3: 200,
  4: 300,
  5: 420,
  6: 560,
  7: 720,
  8: 900,
  9: 1100,
};

export const SPA_COSTS_BY_COUNT: number[] = [60, 180, 360, 600, 900];

export function getGunneryUpgradeCost(currentSkill: number): number | null {
  return GUNNERY_UPGRADE_COSTS[currentSkill] ?? null;
}

export function getPilotingUpgradeCost(currentSkill: number): number | null {
  return PILOTING_UPGRADE_COSTS[currentSkill] ?? null;
}

export function getEdgeUpgradeCost(currentEdge: number): number | null {
  return EDGE_UPGRADE_COSTS[currentEdge] ?? null;
}

export function getNextSPACost(currentAbilitiesCount: number): number | null {
  if (currentAbilitiesCount >= 5) return null; // Лимит: 5 спец-способностей
  return SPA_COSTS_BY_COUNT[currentAbilitiesCount];
}
````

## File: frontend/Dockerfile
````dockerfile
# 1. Этап сборки приложения (Build Stage)
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# 2. Этап раздачи через Nginx (Production Stage)
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
````

## File: frontend/nginx.conf
````ini
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # Проксирование API-запросов к контейнеру бэкенда
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
````

## File: .dockerignore
````
.venv/
__pycache__/
*.pyc
.pytest_cache/
*.db
*.sqlite
*.sqlite3
.git/
node_modules/
frontend/node_modules/
frontend/dist/
````

## File: docker-compose.yml
````yaml
version: '3.8'

services:
  # 1. База данных PostgreSQL
  db:
    image: postgres:16-alpine
    container_name: drcm_db
    restart: always
    environment:
      POSTGRES_DB: chaos_campaign
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgrespassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d chaos_campaign"]
      interval: 5s
      timeout: 5s
      retries: 5

  # 2. Бэкенд FastAPI
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: drcm_backend
    restart: always
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@db:5432/chaos_campaign
      - SECRET_KEY=SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION
      - API_V1_STR=/api/v1
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

  # 3. Фронтенд React SPA
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: drcm_frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
````

## File: Dockerfile
````dockerfile
FROM python:3.12-slim

# Установка менеджера пакетов uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock* ./

# Синхронизация ТОЛЬКО зависимостей (без сборки корневого пакета)
RUN uv sync --frozen --no-install-project || uv sync --no-install-project

# Копирование исходного кода приложения
COPY app/ ./app

EXPOSE 8000

# Запуск FastAPI через uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
````

## File: repomix-output.xml
````xml
This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

<file_summary>
This section contains a summary of this file.

<purpose>
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.
</purpose>

<file_format>
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  - File path as an attribute
  - Full contents of the file
</file_format>

<usage_guidelines>
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.
</usage_guidelines>

<notes>
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: cmake-build-*/**, **/TestData/**, **/*.txt, repomix --ignore **/*.lock, **/package-lock.json, **/pnpm-lock.yaml, **/yarn.lock, **/dist/**, **/build/**, **/coverage/**, **/*.min.*, **/*.map, **/*.svg, **/*.png, **/*.jpg, **/*.pdf, **/*.sqlite, **/*.db, **/*.log*/CMakeLists.txt, **/Autotest_Data/**, **/benchmark/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)
</notes>

</file_summary>

<directory_structure>
app/
  api/
    v1/
      endpoints/
        __init__.py
        auth.py
        contracts.py
        forces.py
        generator.py
        logistics.py
        pilots.py
        tracks.py
      __init__.py
      api.py
    __init__.py
  core/
    __init__.py
    exceptions.py
    security.py
  db/
    models/
      __init__.py
      force.py
      pilot.py
      user.py
    __init__.py
    database.py
  dependencies/
    __init__.py
    auth.py
    campaign.py
    db.py
  schemas/
    __init__.py
    auth.py
    contract.py
    force.py
    generator.py
    logistics.py
    pilot.py
    track.py
  services/
    __init__.py
    force_service.py
    generator_service.py
    logistics_service.py
    negotiation_engine.py
    pilot_service.py
    track_service.py
  tests/
    __init__.py
    conftest.py
    test_force.py
    test_negotiation.py
    test_pilots.py
    test_tracks.py
  __init__.py
  config.py
  main.py
frontend/
  src/
    api/
      client.ts
      services.ts
    components/
      common/
        ProtectedRoute.tsx
      domain/
        ContractNegotiationModal.tsx
        MechStatusBadge.tsx
    pages/
      Auth/
        LoginPage.tsx
        RegisterPage.tsx
      Contracts/
        ContractsPage.tsx
      Dashboard/
        DashboardPage.tsx
      ForceSelection/
        ForceSelectionPage.tsx
      ForceWizard/
        ForceCreationPage.tsx
      Pilot/
        PilotProgressionPage.tsx
    store/
      authStore.ts
    types/
      auth.ts
      index.ts
    utils/
      xpCalculator.ts
    App.css
    App.tsx
    index.css
    main.tsx
  .oxlintrc.json
  index.html
  package.json
  postcss.config.js
  tailwind.config.js
  tsconfig.app.json
  tsconfig.json
  tsconfig.node.json
  vite.config.ts
src/
  chaos_campaign_api/
    __init__.py
.gitignore
.python-version
pyproject.toml
pytest.ini
README.md
</directory_structure>

<files>
This section contains the contents of the repository's files.

<file path="frontend/src/components/domain/ContractNegotiationModal.tsx">
import React, { useState } from 'react';
import { 
  ContractResponse, 
  ContractTerms, 
  CommandRights, 
  SalvageRights 
} from '../../api/services';
import { X, Handshake, AlertTriangle, ShieldCheck } from 'lucide-react';

interface ContractNegotiationModalProps {
  contract: ContractResponse;
  userReputation: number;
  isOpen: boolean;
  onClose: () => void;
  onNegotiate: (terms: ContractTerms) => Promise<void>;
  isPending: boolean;
}

export const ContractNegotiationModal: React.FC<ContractNegotiationModalProps> = ({
  contract,
  userReputation,
  isOpen,
  onClose,
  onNegotiate,
  isPending,
}) => {
  const [terms, setTerms] = useState<ContractTerms>({ ...contract.terms });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    try {
      await onNegotiate(terms);
      onClose();
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Не удалось согласовать новые условия контракта';
      setErrorMessage(msg);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-bt-card border border-bt-border rounded-lg max-w-xl w-full p-6 space-y-6 shadow-2xl">
        {/* Заголовок */}
        <div className="flex justify-between items-center border-b border-bt-border pb-4">
          <div className="flex items-center gap-2">
            <Handshake className="w-6 h-6 text-bt-amber" />
            <h2 className="text-lg font-bold text-white">Переговоры: {contract.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Текущая репутация отряда */}
        <div className="bg-slate-900 p-3 rounded border border-bt-border/60 flex items-center justify-between text-xs font-mono">
          <span className="text-slate-400">Репутация вашего отряда:</span>
          <span className="text-bt-green font-bold flex items-center gap-1">
            <ShieldCheck className="w-4 h-4" /> {userReputation} pts
          </span>
        </div>

        {errorMessage && (
          <div className="bg-red-950/60 border border-bt-red/60 text-red-300 p-3 rounded text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-bt-red" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            {/* Базовая выплата (SP) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Базовая выплата (SP)
              </label>
              <input
                type="number"
                step="50"
                min="0"
                value={terms.base_payment_sp}
                onChange={(e) => setTerms({ ...terms, base_payment_sp: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>

            {/* Накладные расходы (SP) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Накладные расходы (SP)
              </label>
              <input
                type="number"
                step="50"
                min="0"
                value={terms.overhead_sp}
                onChange={(e) => setTerms({ ...terms, overhead_sp: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>

            {/* Права на командование */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Командование
              </label>
              <select
                value={terms.command_rights}
                onChange={(e) => setTerms({ ...terms, command_rights: e.target.value as CommandRights })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-bt-amber"
              >
                <option value={CommandRights.INDEPENDENT}>Independent (Независимое)</option>
                <option value={CommandRights.CO_COMMAND}>Co-Command (Совместное)</option>
                <option value={CommandRights.INTEGRATED}>Integrated (Подчинение)</option>
              </select>
            </div>

            {/* Права на трофеи */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Права на трофеи (Salvage)
              </label>
              <select
                value={terms.salvage_rights}
                onChange={(e) => setTerms({ ...terms, salvage_rights: e.target.value as SalvageRights })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-bt-amber"
              >
                <option value={SalvageRights.FULL}>Full (Полный трофей)</option>
                <option value={SalvageRights.SHARED}>Shared (Разделение)</option>
                <option value={SalvageRights.EXCHANGE}>Exchange (Обмен)</option>
                <option value={SalvageRights.NONE}>None (Без трофеев)</option>
              </select>
            </div>

            {/* Техподдержка (%) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Покрытие ремонта (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={terms.support_rights_percent}
                onChange={(e) => setTerms({ ...terms, support_rights_percent: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>

            {/* Транспорт (%) */}
            <div>
              <label className="block text-[11px] uppercase font-bold text-slate-400 mb-1">
                Покрытие транспорта (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={terms.transport_coverage_percent}
                onChange={(e) => setTerms({ ...terms, transport_coverage_percent: Number(e.target.value) })}
                className="w-full bg-slate-900 border border-bt-border rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-bt-amber font-mono"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-bt-border">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded transition-colors"
            >
              Отмена
            </button>
            <button
              type="submit"
              disabled={isPending}
              className="px-4 py-2 bg-bt-amber hover:bg-amber-600 text-slate-950 font-bold text-xs rounded transition-colors disabled:opacity-50"
            >
              {isPending ? 'Согласование...' : 'Предложить условия'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
</file>

<file path="frontend/src/pages/Contracts/ContractsPage.tsx">
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { contractsApi, ContractResponse, ContractTerms } from '../../api/services';
import { forcesApi } from '../../api/services';
import { ContractNegotiationModal } from '../../components/domain/ContractNegotiationModal';
import { 
  FileText, 
  ShieldCheck, 
  Lock, 
  CheckCircle2, 
  PlusCircle, 
  ChevronLeft, 
  Coins, 
  Filter, 
  Handshake, 
  PenTool 
} from 'lucide-react';

export const ContractsPage: React.FC = () => {
  const { forceId } = useParams<{ forceId?: string }>();
  const queryClient = useQueryClient();
  const [selectedEmployer, setSelectedEmployer] = useState<string>('');
  const [negotiatingContract, setNegotiatingContract] = useState<ContractResponse | null>(null);

  // Загрузка активного отряда
  const { data: force } = useQuery({
    queryKey: ['force', forceId],
    queryFn: () => forcesApi.getForce(forceId!),
    enabled: !!forceId,
  });

  // Загрузка доступных контрактов
  const { data: contracts = [], isLoading, refetch } = useQuery({
    queryKey: ['contracts', selectedEmployer],
    queryFn: () => contractsApi.getAvailableContracts(selectedEmployer ? { employer: selectedEmployer } : undefined),
  });

  // Мутация переговоров
  const negotiateMutation = useMutation({
    mutationFn: ({ contractId, terms }: { contractId: string; terms: ContractTerms }) =>
      contractsApi.negotiateContract(contractId, { requested_terms: terms }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contracts'] });
    },
  });

  // Мутация подписания контракта
  const signMutation = useMutation({
    mutationFn: (contractId: string) => contractsApi.signContract(contractId, forceId!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contracts'] });
      queryClient.invalidateQueries({ queryKey: ['force', forceId] });
      alert('Контракт успешно подписан!');
    },
  });

  // Генерация процедурного контракта
  const generateMutation = useMutation({
    mutationFn: contractsApi.generateContract,
    onSuccess: () => {
      refetch();
    },
  });

  const userReputation = force?.reputation_score || 1;

  return (
    <div className="min-h-screen bg-bt-bg text-white flex flex-col font-sans">
      {/* Шапка навигации */}
      <header className="bg-bt-card border-b border-bt-border px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Link
            to={forceId ? `/forces/${forceId}` : '/'}
            className="p-2 bg-slate-900 border border-bt-border rounded text-slate-400 hover:text-white transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </Link>
          <FileText className="w-8 h-8 text-bt-amber" />
          <div>
            <h1 className="text-xl font-bold uppercase tracking-wide">Доска Контрактов</h1>
            <p className="text-xs text-slate-400">
              Выбор военных заказов в секторе Draconis Reach[cite: 2]
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
            className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 border border-bt-border text-bt-amber font-bold px-3 py-2 rounded text-xs transition-colors"
          >
            <PlusCircle className="w-4 h-4" /> Сгенерировать новый заказ
          </button>
        </div>
      </header>

      {/* Панель фильтрации */}
      <div className="bg-slate-900/60 border-b border-bt-border px-6 py-3 flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-bt-amber" />
          <span className="text-xs uppercase font-bold text-slate-400">Наниматель:</span>
          <select
            value={selectedEmployer}
            onChange={(e) => setSelectedEmployer(e.target.value)}
            className="bg-slate-900 border border-bt-border rounded px-3 py-1 text-xs text-white focus:outline-none focus:border-bt-amber"
          >
            <option value="">Все фракции</option>
            <option value="Draconis Combine">Draconis Combine</option>
            <option value="Federated Suns">Federated Suns</option>
            <option value="Mercenary">Mercenary Market</option>
          </select>
        </div>

        {force && (
          <div className="text-xs font-mono">
            <span className="text-slate-400">Репутация отряда {force.name}: </span>
            <span className="text-bt-amber font-bold">{force.reputation_score} pts</span>
          </div>
        )}
      </div>

      {/* Список контрактов */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto">
        {isLoading ? (
          <div className="text-center text-bt-amber py-12 font-mono animate-pulse">
            Поиск военных контрактов...
          </div>
        ) : contracts.length === 0 ? (
          <div className="bg-bt-card border border-bt-border p-8 rounded-lg text-center max-w-md mx-auto my-12">
            <p className="text-slate-400 text-sm mb-4">Доступные контракты не найдены.</p>
            <button
              onClick={() => generateMutation.mutate()}
              className="bg-bt-amber text-slate-950 font-bold px-4 py-2 rounded text-xs hover:bg-amber-600 transition-colors"
            >
              Сгенерировать случайный контракт
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {contracts.map((contract) => {
              const meetsReputation = userReputation >= contract.required_reputation;

              return (
                <div
                  key={contract.id}
                  className="bg-bt-card border border-bt-border rounded-lg p-5 flex flex-col justify-between space-y-4 shadow-xl"
                >
                  <div>
                    {/* Заголовок и индикатор репутации */}
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold text-white text-base">{contract.title}</h3>
                        <p className="text-xs font-mono text-bt-amber">{contract.location_hot_spot}</p>
                      </div>
                      {meetsReputation ? (
                        <span className="flex items-center gap-1 text-[10px] bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 font-bold px-2 py-0.5 rounded" title="Репутация подходит">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Доступен
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-[10px] bg-red-950/80 border border-bt-red/40 text-red-300 font-bold px-2 py-0.5 rounded" title="Недостаточно репутации">
                          <Lock className="w-3.5 h-3.5" /> Rep {contract.required_reputation}
                        </span>
                      )}
                    </div>

                    {/* Фракции */}
                    <div className="text-xs text-slate-400 space-y-0.5 my-3 bg-slate-900/60 p-2.5 rounded border border-bt-border/40">
                      <div>
                        <span className="text-slate-500 font-bold uppercase text-[10px]">Наниматель:</span>{' '}
                        <span className="text-slate-200">{contract.employer}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 font-bold uppercase text-[10px]">Противник:</span>{' '}
                        <span className="text-bt-red">{contract.target_faction}</span>
                      </div>
                    </div>

                    {/* Финансовые условия */}
                    <div className="grid grid-cols-2 gap-2 bg-slate-900 p-3 rounded border border-bt-border/50 text-xs text-center font-mono my-3">
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Выплата</span>
                        <span className="text-bt-amber font-bold">{contract.terms.base_payment_sp} SP</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Оверхед</span>
                        <span className="text-white font-bold">{contract.terms.overhead_sp} SP</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Командование</span>
                        <span className="text-slate-300 text-[10px] font-sans">{contract.terms.command_rights}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[9px] uppercase font-sans">Трофеи</span>
                        <span className="text-slate-300 text-[10px] font-sans">{contract.terms.salvage_rights}</span>
                      </div>
                    </div>
                  </div>

                  {/* Кнопки действий */}
                  <div className="pt-3 border-t border-bt-border/60 flex items-center gap-2">
                    <button
                      onClick={() => setNegotiatingContract(contract)}
                      className="flex-1 flex items-center justify-center gap-1 bg-slate-800 hover:bg-slate-700 border border-bt-border text-slate-200 font-bold py-2 rounded text-xs transition-colors"
                    >
                      <Handshake className="w-3.5 h-3.5 text-bt-amber" /> Переговоры
                    </button>

                    {forceId && (
                      <button
                        onClick={() => signMutation.mutate(contract.id)}
                        disabled={!meetsReputation || contract.is_signed || signMutation.isPending}
                        className="flex-1 flex items-center justify-center gap-1 bg-bt-amber hover:bg-amber-600 text-slate-950 font-bold py-2 rounded text-xs transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                      >
                        <PenTool className="w-3.5 h-3.5" /> {contract.is_signed ? 'Подписан' : 'Подписать'}
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* Модалка переговоров */}
      {negotiatingContract && (
        <ContractNegotiationModal
          contract={negotiatingContract}
          userReputation={userReputation}
          isOpen={!!negotiatingContract}
          onClose={() => setNegotiatingContract(null)}
          isPending={negotiateMutation.isPending}
          onNegotiate={async (terms) => {
            await negotiateMutation.mutateAsync({
              contractId: negotiatingContract.id,
              terms,
            });
          }}
        />
      )}
    </div>
  );
};
</file>

<file path="frontend/src/pages/Pilot/PilotProgressionPage.tsx">
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
</file>

<file path="frontend/src/utils/xpCalculator.ts">
export const GUNNERY_UPGRADE_COSTS: Record<number, number> = {
  4: 300,  // 4 -> 3
  3: 700,  // 3 -> 2
  2: 1200, // 2 -> 1
  1: 2200, // 1 -> 0
};

export const PILOTING_UPGRADE_COSTS: Record<number, number> = {
  5: 100,  // 5 -> 4
  4: 200,  // 4 -> 3
  3: 700,  // 3 -> 2
  2: 1200, // 2 -> 1
};

export const EDGE_UPGRADE_COSTS: Record<number, number> = {
  1: 60,   // 1 -> 2
  2: 120,
  3: 200,
  4: 300,
  5: 420,
  6: 560,
  7: 720,
  8: 900,
  9: 1100,
};

export const SPA_COSTS_BY_COUNT: number[] = [60, 180, 360, 600, 900];

export function getGunneryUpgradeCost(currentSkill: number): number | null {
  return GUNNERY_UPGRADE_COSTS[currentSkill] ?? null;
}

export function getPilotingUpgradeCost(currentSkill: number): number | null {
  return PILOTING_UPGRADE_COSTS[currentSkill] ?? null;
}

export function getEdgeUpgradeCost(currentEdge: number): number | null {
  return EDGE_UPGRADE_COSTS[currentEdge] ?? null;
}

export function getNextSPACost(currentAbilitiesCount: number): number | null {
  if (currentAbilitiesCount >= 5) return null; // Лимит: 5 спец-способностей
  return SPA_COSTS_BY_COUNT[currentAbilitiesCount];
}
</file>

<file path="app/api/v1/endpoints/__init__.py">

</file>

<file path="app/api/v1/endpoints/auth.py">
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.db.models.user import UserModel
from app.schemas.auth import Token, UserRegister, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Регистрация командира")
async def register_user(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрирует нового командира отряда в базе данных.
    
    * **201 Created**: Пользователь успешно создан.
    * **400 Bad Request**: Имя пользователя уже занято.
    """
    stmt = select(UserModel).where(UserModel.username == user_in.username)
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    new_user = UserModel(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(new_user)
    await db.flush()
    return new_user


@router.post("/token", response_model=Token, summary="Получение JWT токена")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентифицирует пользователя по логину/паролю и выдает JWT токен формата Bearer.
    """
    stmt = select(UserModel).where(UserModel.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")
</file>

<file path="app/api/v1/endpoints/contracts.py">
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.contract import ContractNegotiationOffer, ContractResponse
from app.schemas.force import Faction
from app.services.generator_service import GeneratorService
from app.services.negotiation_engine import NegotiationEngine

router = APIRouter()


@router.get("/available", response_model=List[ContractResponse], summary="Поиск доступных контрактов")
async def get_available_contracts(
    employer: Optional[Faction] = Query(None, description="Фильтр по нанимателю"),
    location: Optional[str] = Query(None, min_length=2, description="Локация Hot Spot"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: UserModel = Depends(get_current_user)
):
    """Возвращает список доступных контрактов с поддержкой фильтрации и пагинации."""
    # Генерация примеров контрактов для каталога
    contracts = [
        GeneratorService.generate_random_contract(
            employer=employer or Faction.DRACONIS_COMBINE,
            target_faction=Faction.FEDERATED_SUNS
        ) for _ in range(limit)
    ]
    return contracts


@router.post("/{contract_id}/negotiate", summary="Переговоры по условиям контракта")
async def negotiate_contract(
    contract_id: str,
    offer: ContractNegotiationOffer,
    force_id: str = Query(..., description="ID отряда"),
    force: ForceModel = Depends(verify_force_ownership)
):
    """
    Проверяет запрашиваемые условия контракта с Очками Репутации отряда.
    
    * **400 Bad Request**: Недостаточно репутации (`ReputationRequirementNotMetError`).
    """
    mock_contract = GeneratorService.generate_random_contract()
    mock_contract.id = contract_id

    NegotiationEngine.validate_negotiation_offer(
        force=force, contract=mock_contract, requested_terms=offer.requested_terms
    )
    mock_contract.terms = offer.requested_terms
    return {"status": "terms_accepted", "contract": mock_contract}


@router.post("/{contract_id}/sign", summary="Подписание контракта")
async def sign_contract(
    contract_id: str,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Подписывает контракт и закрепляет его за отрядом."""
    return {"status": "contract_signed", "contract_id": contract_id, "force_id": force.id}
</file>

<file path="app/api/v1/endpoints/generator.py">
from fastapi import APIRouter, Depends
from app.schemas.contract import ContractResponse
from app.schemas.generator import ContractGenerateRequest
from app.services.generator_service import GeneratorService

router = APIRouter()


@router.post("/contract", response_model=ContractResponse, summary="Процедурная генерация контракта")
async def generate_contract(request: ContractGenerateRequest):
    """Создает случайный контракт по правилам книги Hot Spots."""
    return GeneratorService.generate_random_contract(
        employer=request.employer,
        target_faction=request.target_faction
    )
</file>

<file path="app/api/v1/endpoints/logistics.py">
import random
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import Faction, WeightClass
from app.schemas.logistics import PurchaseUnitRequest, RepairRequest, ScrapUnitRequest
from app.services.logistics_service import LogisticsService

router = APIRouter()


@router.post("/repair", summary="Ремонт техники за SP")
async def repair_unit(
    request: RepairRequest,
    sp_cost: int = Query(50, ge=0),
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Восстанавливает поврежденный мех до статуса OPERATIONAL за SP."""
    try:
        repaired_unit = await LogisticsService.repair_unit(
            db=db, force=force, unit_id=request.unit_id, sp_cost=sp_cost
        )
        return {"status": "repaired", "unit_id": repaired_unit.id, "remaining_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/scrap", summary="Утилизация уничтоженной техники на лом")
async def scrap_unit(
    request: ScrapUnitRequest,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Списывает полностью уничтоженный мех (TRULY_DESTROYED) и зачисляет 25% стоимости в SP."""
    try:
        sp_yield = await LogisticsService.scrap_unit(db=db, force=force, unit_id=request.unit_id)
        return {"status": "scrapped", "sp_earned": sp_yield, "total_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/buy-unit", summary="Покупка новой техники")
async def buy_unit(
    request: PurchaseUnitRequest,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Приобретает новый мех и привязывает его к ростеру отряда."""
    try:
        new_unit = await LogisticsService.buy_unit(db=db, force=force, request=request)
        return {"status": "purchased", "unit": new_unit, "remaining_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/rat-roll", summary="Ролл по таблицам RAT (Random Assignment Tables)")
async def rat_roll(
    faction: Faction = Query(...),
    weight_class: WeightClass = Query(...),
    unit_rating: str = Query("Scale 1", pattern=r"^Scale [1-3]$")
):
    """Генерирует случайный мех по таблицам RAT региона Draconis Reach."""
    sample_mechs = {
        WeightClass.LIGHT: [("Panther", "PTH-9R"), ("Jenner", "JR7-D"), ("Locust", "LCT-1E")],
        WeightClass.MEDIUM: [("Starslayer", "STAGE-3C"), ("Phoenix Hawk", "PXH-1K"), ("Centurion", "CN9-A")],
        WeightClass.HEAVY: [("Dragon", "DRG-1N"), ("Catapult", "CPLT-C1"), ("Grasshopper", "GHR-5H")],
        WeightClass.ASSAULT: [("Awesome", "AWS-8Q"), ("BattleMaster", "BLR-1D"), ("Stalker", "STK-3H")],
    }
    chassis, model = random.choice(sample_mechs[weight_class])
    return {
        "faction": faction,
        "weight_class": weight_class,
        "unit_rating": unit_rating,
        "rolled_mech": {"chassis": chassis, "model": model}
    }
</file>

<file path="app/api/v1/endpoints/pilots.py">
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.schemas.pilot import NamedPilot, PilotUpgradeRequest
from app.services.pilot_service import PilotService

router = APIRouter()


@router.get("/{pilot_id}", response_model=NamedPilot, summary="Информация о пилоте")
async def get_pilot(
    pilot_id: str = Path(..., description="UUID пилота"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Возвращает карточку пилота из СУБД."""
    stmt = select(PilotModel).where(PilotModel.id == pilot_id)
    res = await db.execute(stmt)
    pilot = res.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пилот не найден")
    return pilot


@router.post("/{pilot_id}/upgrade", response_model=NamedPilot, summary="Прокачка пилота за XP")
async def upgrade_pilot(
    request: PilotUpgradeRequest,
    pilot_id: str = Path(..., description="UUID пилота"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Транзакционно улучшает навык Gunnery/Piloting, добавляет Edge или покупает SPA за XP.
    
    * **400 Bad Request**: Недостаточно XP (`InsufficientXPError`) или достигнут предел.
    """
    stmt = select(PilotModel).where(PilotModel.id == pilot_id)
    res = await db.execute(stmt)
    pilot = res.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пилот не найден")

    try:
        return await PilotService.upgrade_pilot(db=db, pilot=pilot, request=request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
</file>

<file path="app/api/v1/__init__.py">

</file>

<file path="app/api/v1/api.py">
from fastapi import APIRouter
from app.api.v1.endpoints import auth, contracts, forces, generator, logistics, pilots, tracks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(forces.router, prefix="/forces", tags=["Forces"])
api_router.include_router(pilots.router, prefix="/pilots", tags=["Pilots"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
api_router.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])
api_router.include_router(generator.router, prefix="/generator", tags=["Generator"])
</file>

<file path="app/api/__init__.py">

</file>

<file path="app/core/__init__.py">

</file>

<file path="app/core/security.py">
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
import bcrypt
import jwt
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие открытого пароля сохраненному хэшу."""
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """Генерирует хэш bcrypt для пароля с обрезкой до 72 байт."""
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Создает подписанный JWT токен доступа."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "commander_id": str(subject),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
</file>

<file path="app/db/models/__init__.py">
from app.db.models.user import UserModel
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel

__all__ = ["UserModel", "ForceModel", "MechUnitModel", "PilotModel"]
</file>

<file path="app/db/__init__.py">

</file>

<file path="app/db/database.py">
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    """Базовый декларативный класс для всех моделей СУБД."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency для инъекции асинхронной сессии базы данных.
    Автоматически фиксирует транзакцию при успехе или откатывает при ошибке.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
</file>

<file path="app/dependencies/__init__.py">

</file>

<file path="app/dependencies/auth.py">
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.database import get_db
from app.db.models.user import UserModel
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserModel:
    """Извлекает и валидирует текущего пользователя из JWT токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        commander_id: str = payload.get("sub") or payload.get("commander_id")
        if commander_id is None:
            raise credentials_exception
        token_data = TokenData(commander_id=commander_id)
    except jwt.PyJWTError:
        raise credentials_exception

    stmt = select(UserModel).where(UserModel.id == token_data.commander_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Пользователь неактивен"
        )

    return user
</file>

<file path="app/dependencies/campaign.py">
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user


async def verify_force_ownership(
    force_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ForceModel:
    """Проверяет существование отряда в СУБД и права доступа текущего пользователя."""
    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force_id)
        .options(
            selectinload(ForceModel.units),
            selectinload(ForceModel.pilots)
        )
    )
    result = await db.execute(stmt)
    force = result.scalar_one_or_none()

    if force is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Отряд с ID '{force_id}' не найден"
        )

    if force.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для управления этим отрядом"
        )

    return force
</file>

<file path="app/dependencies/db.py">
from app.db.database import get_db

__all__ = ["get_db"]
</file>

<file path="app/schemas/__init__.py">
from app.schemas.auth import Token, TokenData, UserLogin, UserRegister, UserResponse
from app.schemas.pilot import NamedPilot, SkillUpgrade, EdgeUpgrade, AbilityUpgrade, PilotUpgradeRequest
from app.schemas.force import Faction, UnitStatus, WeightClass, MechUnit, ForceCreate, ForceResponse, AssignPilotRequest
from app.schemas.contract import CommandRights, SalvageRights, ContractTerms, ContractNegotiationOffer, ContractResponse
from app.schemas.track import PilotTrackPerformance, TrackCompletionRequest, XPAllocationResult, TrackCompletionResponse
from app.schemas.logistics import RepairRequest, ScrapUnitRequest, PurchaseUnitRequest, RATRollQuery
from app.schemas.generator import ContractGenerateRequest

__all__ = [
    "Token", "TokenData", "UserLogin", "UserRegister", "UserResponse",
    "NamedPilot", "SkillUpgrade", "EdgeUpgrade", "AbilityUpgrade", "PilotUpgradeRequest",
    "Faction", "UnitStatus", "WeightClass", "MechUnit", "ForceCreate", "ForceResponse", "AssignPilotRequest",
    "CommandRights", "SalvageRights", "ContractTerms", "ContractNegotiationOffer", "ContractResponse",
    "PilotTrackPerformance", "TrackCompletionRequest", "XPAllocationResult", "TrackCompletionResponse",
    "RepairRequest", "ScrapUnitRequest", "PurchaseUnitRequest", "RATRollQuery",
    "ContractGenerateRequest",
]
</file>

<file path="app/schemas/auth.py">
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Token(BaseModel):
    """Ответ API с JWT токеном доступа."""
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")


class TokenData(BaseModel):
    """Данные, зашифрованные внутри JWT токена."""
    commander_id: Optional[str] = Field(None, description="UUID командира в БД")


class UserLogin(BaseModel):
    """Схема входа пользователя."""
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "commander_vance"})
    password: str = Field(..., min_length=4, json_schema_extra={"example": "strongpassword123"})


class UserRegister(BaseModel):
    """Схема регистрации нового командира в СУБД."""
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "commander_vance"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "strongpassword123"})


class UserResponse(BaseModel):
    """Публичные данные пользователя."""
    id: str = Field(..., description="Уникальный UUID пользователя в БД")
    username: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
</file>

<file path="app/schemas/generator.py">
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.force import Faction


class ContractGenerateRequest(BaseModel):
    """Параметры процедуры генерации случайного контракта."""
    employer: Optional[Faction] = Field(None, description="Целевой наниматель")
    target_faction: Optional[Faction] = Field(None, description="Вражеская фракция")
    location_hot_spot: Optional[str] = Field(None, description="Локация в Draconis Reach")
</file>

<file path="app/schemas/logistics.py">
from pydantic import BaseModel, Field
from app.schemas.force import Faction, WeightClass


class RepairRequest(BaseModel):
    """Запрос на ремонт поврежденной техники за SP."""
    unit_id: str = Field(..., description="ID поврежденного меха")


class ScrapUnitRequest(BaseModel):
    """Запрос на утилизацию уничтоженной техники (TRULY_DESTROYED) на лом."""
    unit_id: str = Field(..., description="ID техники для утилизации в SP в БД")


class PurchaseUnitRequest(BaseModel):
    """Запрос на покупку новой единицы техники."""
    chassis: str = Field(..., json_schema_extra={"example": "Catapult"})
    model: str = Field(..., json_schema_extra={"example": "CPLT-C1"})
    tonnage: int = Field(..., ge=20, le=100, json_schema_extra={"example": 65})
    weight_class: WeightClass = Field(..., json_schema_extra={"example": WeightClass.HEAVY})
    bv2: int = Field(..., ge=100, le=5000, json_schema_extra={"example": 1399})
    cost_sp: int = Field(..., ge=0, json_schema_extra={"example": 300})


class RATRollQuery(BaseModel):
    """Параметры генерации случайной техники по RAT-таблицам."""
    faction: Faction
    unit_rating: str = Field(..., pattern=r"^Scale [1-3]$", description="Рейтинг подразделения (Scale 1, Scale 2, Scale 3)")
    weight_class: WeightClass
</file>

<file path="app/schemas/pilot.py">
from typing import Annotated, List, Literal, Union, Optional
from pydantic import BaseModel, Field, ConfigDict


class NamedPilot(BaseModel):
    """Модель именного пилота отряда наемников."""
    id: str = Field(..., description="Уникальный UUID пилота в БД")
    force_id: Optional[str] = Field(None, description="ID отряда в БД")
    name: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "Maverick Banderas"})
    gunnery: int = Field(default=4, ge=0, le=8, description="Навык стрельбы (чем ниже, тем лучше)")
    piloting: int = Field(default=5, ge=0, le=8, description="Навык пилотирования (чем ниже, тем лучше)")
    
    # Система опыта (XP)
    experience_points: int = Field(default=0, ge=0, description="Доступные очки опыта (XP)")
    total_xp_earned: int = Field(default=0, ge=0, description="Всего заработано XP за кампанию")
    
    # Способности и Edge
    edge_points: int = Field(default=1, ge=0, le=10, description="Текущее значение Edge (0-10)")
    special_abilities: List[str] = Field(
        default_factory=list, 
        json_schema_extra={"example": ["Overcharge", "Dodge", "Marksman"]},
        description="Купленные спец-способности (SPAs) и способности Edge"
    )
    is_temporary_hire: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)


# --- Discriminated Unions для полиморфных запросов на улучшение пилота ---

class SkillUpgrade(BaseModel):
    """Улучшение навыка стрельбы или пилотирования."""
    upgrade_type: Literal["gunnery", "piloting"]


class EdgeUpgrade(BaseModel):
    """Покупка дополнительного очка Edge."""
    upgrade_type: Literal["edge"]


class AbilityUpgrade(BaseModel):
    """Покупка специальной способности (SPA)."""
    upgrade_type: Literal["ability"]
    ability_name: str = Field(..., min_length=2, description="Название спец-способности (SPA)")


PilotUpgradeRequest = Annotated[
    Union[SkillUpgrade, EdgeUpgrade, AbilityUpgrade], 
    Field(discriminator="upgrade_type")
]
</file>

<file path="app/services/__init__.py">
from app.services.pilot_service import PilotService
from app.services.negotiation_engine import NegotiationEngine
from app.services.force_service import ForceService
from app.services.track_service import TrackService
from app.services.logistics_service import LogisticsService
from app.services.generator_service import GeneratorService

__all__ = [
    "PilotService",
    "NegotiationEngine",
    "ForceService",
    "TrackService",
    "LogisticsService",
    "GeneratorService",
]
</file>

<file path="app/services/logistics_service.py">
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.schemas.force import UnitStatus
from app.schemas.logistics import PurchaseUnitRequest


class LogisticsService:
    @staticmethod
    async def repair_unit(db: AsyncSession, force: ForceModel, unit_id: str, sp_cost: int) -> MechUnitModel:
        """Ремонтирует поврежденный мех за SP, возвращая ему статус OPERATIONAL."""
        if force.support_points < sp_cost:
            raise ValueError(f"Недостаточно SP для ремонта. Требуется: {sp_cost}, доступно: {force.support_points}")

        stmt = select(MechUnitModel).where(MechUnitModel.id == unit_id, MechUnitModel.force_id == force.id)
        res = await db.execute(stmt)
        unit = res.scalar_one_or_none()

        if not unit:
            raise ValueError("Техника не найдена в отряде")

        force.support_points -= sp_cost
        unit.status = UnitStatus.OPERATIONAL
        db.add_all([force, unit])
        await db.flush()
        return unit

    @staticmethod
    async def scrap_unit(db: AsyncSession, force: ForceModel, unit_id: str) -> int:
        """
        Утилизирует уничтоженный мех (TRULY_DESTROYED) на лом.
        Зачисляет 25% его базовой стоимости в SP и удаляет объект из БД.
        """
        stmt = select(MechUnitModel).where(MechUnitModel.id == unit_id, MechUnitModel.force_id == force.id)
        res = await db.execute(stmt)
        unit = res.scalar_one_or_none()

        if not unit:
            raise ValueError("Техника не найдена в отряде")
        if unit.status != UnitStatus.TRULY_DESTROYED:
            raise ValueError("На лом можно распилить только полностью уничтоженную технику (TRULY_DESTROYED)")

        # Расчет 25% стоимости от тоннажа/BV2 в SP
        sp_yield = int((unit.tonnage * 10) * 0.25)
        force.support_points += sp_yield

        await db.delete(unit)
        db.add(force)
        await db.flush()
        return sp_yield

    @staticmethod
    async def buy_unit(db: AsyncSession, force: ForceModel, request: PurchaseUnitRequest) -> MechUnitModel:
        """Покупка новой техники за SP."""
        if force.support_points < request.cost_sp:
            raise ValueError(f"Недостаточно SP для покупки. Требуется: {request.cost_sp}, доступно: {force.support_points}")

        force.support_points -= request.cost_sp
        new_unit = MechUnitModel(
            force_id=force.id,
            chassis=request.chassis,
            model=request.model,
            tonnage=request.tonnage,
            weight_class=request.weight_class,
            bv2=request.bv2,
            status=UnitStatus.OPERATIONAL
        )
        db.add_all([force, new_unit])
        await db.flush()
        return new_unit
</file>

<file path="app/services/pilot_service.py">
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from app.core.exceptions import InsufficientXPError
from app.db.models.pilot import PilotModel
from app.schemas.pilot import (
    AbilityUpgrade,
    EdgeUpgrade,
    PilotUpgradeRequest,
    SkillUpgrade,
)

# Нелинейные таблицы стоимости прокачки пилотов (в XP) согласно спецификации v3.0
GUNNERY_UPGRADE_COSTS = {4: 300, 3: 700, 2: 1200, 1: 2200}
PILOTING_UPGRADE_COSTS = {5: 100, 4: 200, 3: 700, 2: 1200}
EDGE_UPGRADE_COSTS = {
    1: 60, 2: 120, 3: 200, 4: 300, 5: 420,
    6: 560, 7: 720, 8: 900, 9: 1100
}
SPA_COST_TABLE = [60, 180, 360, 600, 900]


class PilotService:
    @staticmethod
    async def upgrade_pilot(
        db: AsyncSession, 
        pilot: PilotModel, 
        request: PilotUpgradeRequest
    ) -> PilotModel:
        """
        Прокачивает характеристики пилота за XP в рамках асинхронной транзакции БД.
        
        :raises InsufficientXPError: Если у пилота недостаточно experience_points.
        :raises ValueError: Если достигнут лимит развития параметра.
        """
        if isinstance(request, SkillUpgrade):
            if request.upgrade_type == "gunnery":
                cost = GUNNERY_UPGRADE_COSTS.get(pilot.gunnery)
                if cost is None:
                    raise ValueError("Достигнут максимальный навык Gunnery (0)")
                if pilot.experience_points < cost:
                    raise InsufficientXPError(required=cost, available=pilot.experience_points)
                pilot.experience_points -= cost
                pilot.gunnery -= 1

            elif request.upgrade_type == "piloting":
                cost = PILOTING_UPGRADE_COSTS.get(pilot.piloting)
                if cost is None:
                    raise ValueError("Достигнут максимальный навык Piloting (1)")
                if pilot.experience_points < cost:
                    raise InsufficientXPError(required=cost, available=pilot.experience_points)
                pilot.experience_points -= cost
                pilot.piloting -= 1

        elif isinstance(request, EdgeUpgrade):
            cost = EDGE_UPGRADE_COSTS.get(pilot.edge_points)
            if cost is None:
                raise ValueError("Достигнуто максимальное значение Edge (10)")
            if pilot.experience_points < cost:
                raise InsufficientXPError(required=cost, available=pilot.experience_points)
            pilot.experience_points -= cost
            pilot.edge_points += 1

        elif isinstance(request, AbilityUpgrade):
            ability_name = request.ability_name.strip()
            if not ability_name:
                raise ValueError("Название способности не может быть пустым")

            current_abilities = list(getattr(pilot, "special_abilities", []) or [])
            if len(current_abilities) >= 5:
                raise ValueError("Достигнут лимит в 5 специальных способностей")

            if ability_name in current_abilities:
                raise ValueError("Эта способность уже изучена пилотом")

            ability_index = min(len(current_abilities), len(SPA_COST_TABLE) - 1)
            cost = SPA_COST_TABLE[ability_index]

            if pilot.experience_points < cost:
                raise InsufficientXPError(required=cost, available=pilot.experience_points)

            pilot.experience_points -= cost
            current_abilities.append(ability_name)
            pilot.special_abilities = current_abilities
            flag_modified(pilot, "special_abilities")

        db.add(pilot)
        await db.commit()
        await db.refresh(pilot)
        return pilot
</file>

<file path="app/tests/__init__.py">

</file>

<file path="app/tests/test_force.py">
import pytest
from httpx import AsyncClient
from app.config import settings


async def test_create_force_v6_success(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Iron Hand Mercenaries",
        "sponsoring_faction": "Draconis Combine",
        "starting_pilot_names": ["Kenshin", "Saito"],
        "selected_mechs": [
            {"chassis": "Panther", "model": "PNT-9R", "tonnage": 35, "weight_class": "Light", "bv2": 769},
            {"chassis": "Dragon", "model": "DRG-1N", "tonnage": 60, "weight_class": "Heavy", "bv2": 1125}
        ]
    }

    response = await client.post(f"{settings.API_V1_STR}/forces/", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["support_points"] == 3000
    assert data["reputation_score"] == 1
    assert len(data["pilots"]) == 2
    assert data["pilots"][0]["experience_points"] == 150
    assert len(data["units"]) == 2


async def test_create_force_v6_exceed_bv2_limit(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Heavy Assault Mercs",
        "sponsoring_faction": "Draconis Combine",
        "starting_pilot_names": ["Pilot A", "Pilot B"],
        "selected_mechs": [
            {"chassis": "Atlas", "model": "AS7-D", "tonnage": 100, "weight_class": "Assault", "bv2": 1897},
            {"chassis": "Awesome", "model": "AWS-8Q", "tonnage": 80, "weight_class": "Assault", "bv2": 1605}
        ]  # Итого: 3502 BV2 > 3000 BV2
    }

    response = await client.post(f"{settings.API_V1_STR}/forces/", json=payload, headers=auth_headers)

    assert response.status_code == 422
</file>

<file path="app/__init__.py">

</file>

<file path="frontend/src/api/client.ts">
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
</file>

<file path="frontend/src/components/common/ProtectedRoute.tsx">
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const ProtectedRoute: React.FC = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
</file>

<file path="frontend/src/components/domain/MechStatusBadge.tsx">
import React from 'react';
import { UnitStatus } from '../../types';

interface MechStatusBadgeProps {
  status: UnitStatus;
}

export const MechStatusBadge: React.FC<MechStatusBadgeProps> = ({ status }) => {
  switch (status) {
    case UnitStatus.OPERATIONAL:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-emerald-950/80 text-emerald-400 border border-emerald-500/40">
          Боеспособен
        </span>
      );
    case UnitStatus.DAMAGED:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-amber-950/80 text-amber-400 border border-amber-500/40">
          Поврежден
        </span>
      );
    case UnitStatus.DESTROYED:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-orange-950/80 text-orange-400 border border-orange-500/40">
          Уничтожен
        </span>
      );
    case UnitStatus.TRULY_DESTROYED:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-red-950/80 text-red-400 border border-red-500/40 animate-pulse">
          Полный лом
        </span>
      );
    default:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-slate-800 text-slate-400">
          {status}
        </span>
      );
  }
};
</file>

<file path="frontend/src/pages/Auth/LoginPage.tsx">
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
</file>

<file path="frontend/src/pages/Auth/RegisterPage.tsx">
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authApi } from '../../api/services';
import { Shield, Lock, User as UserIcon } from 'lucide-react';

export const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await authApi.register({ username, password });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
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
            РЕГИСТРАЦИЯ КОМАНДИРА
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
              Имя пользователя / Позывной
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
            {isLoading ? 'Создание записи...' : 'Создать учетную запись'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate-400">
          Уже зарегистрированы?{' '}
          <Link to="/login" className="text-bt-amber hover:underline">
            Войти
          </Link>
        </p>
      </div>
    </div>
  );
};
</file>

<file path="frontend/src/pages/ForceSelection/ForceSelectionPage.tsx">
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
</file>

<file path="frontend/src/pages/ForceWizard/ForceCreationPage.tsx">
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
</file>

<file path="frontend/src/store/authStore.ts">
import { create } from 'zustand';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  setToken: (token) => {
    if (token) {
      localStorage.setItem('token', token);
      set({ token, isAuthenticated: true });
    } else {
      localStorage.removeItem('token');
      set({ token: null, isAuthenticated: false });
    }
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, isAuthenticated: false });
  },
}));
</file>

<file path="frontend/src/types/auth.ts">
export interface User {
  id: string;
  username: string;
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}
</file>

<file path="frontend/src/types/index.ts">
export const Faction = {
  DRACONIS_COMBINE: "Draconis Combine",
  FEDERATED_SUNS: "Federated Suns",
  RAVEN_ALLIANCE: "Raven Alliance",
  CLAN_SEA_FOX: "Clan Sea Fox",
  REPUBLIC_OF_THE_SPHERE: "Republic of the Sphere",
  MERCENARY: "Mercenary"
} as const;

export type Faction = (typeof Faction)[keyof typeof Faction];

export const UnitStatus = {
  OPERATIONAL: "Operational",
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  TRULY_DESTROYED: "Truly Destroyed"
} as const;
export type UnitStatus = (typeof UnitStatus)[keyof typeof UnitStatus];

export const WeightClass = {
  LIGHT: "Light",
  MEDIUM: "Medium",
  HEAVY: "Heavy",
  ASSAULT: "Assault"
} as const;
export type WeightClass = (typeof WeightClass)[keyof typeof WeightClass];

export interface NamedPilot {
  id: string;
  force_id?: string | null;
  name: string;
  gunnery: number;
  piloting: number;
  experience_points: number;
  total_xp_earned: number;
  edge_points: number;
  special_abilities: string[];
  is_temporary_hire: boolean;
}

export interface MechUnit {
  id: string;
  force_id?: string | null;
  chassis: string;
  model: string;
  tonnage: number;
  weight_class: WeightClass;
  bv2: number;
  status: UnitStatus;
  assigned_pilot_id?: string | null;
}

export interface StartingMechSelection {
  chassis: string;
  model: string;
  tonnage: number;
  weight_class: WeightClass;
  bv2: number;
}

export interface ForceCreate {
  name: string;
  sponsoring_faction: Faction;
  starting_pilot_names: [string, string];
  selected_mechs: StartingMechSelection[];
}

export interface ForceResponse {
  id: string;
  owner_id: string;
  name: string;
  sponsoring_faction: Faction;
  support_points: number;
  reputation_score: number;
  units: MechUnit[];
  pilots: NamedPilot[];
}

export interface AssignPilotRequest {
  unit_id: string;
  pilot_id?: string | null;
}

export interface StartingFactionOption {
  faction: Faction;
  display_name: string;
  description: string;
  available_rat_mechs: StartingMechSelection[];
}

export interface StartingOptionsResponse {
  available_factions: StartingFactionOption[];
  max_starting_mechs: number;
  max_starting_bv2: number;
  starting_sp: number;
  starting_reputation: number;
  starting_pilots_count: number;
  starting_xp_per_pilot: number;
}

export interface NamedPilot {
  id: string;
  force_id?: string | null;
  name: string;
  gunnery: number; 
  piloting: number; 
  experience_points: number;
  total_xp_earned: number;
  edge_points: number;
  special_abilities: string[];
  is_temporary_hire: boolean;
}

export type SkillUpgrade = {
  upgrade_type: "gunnery" | "piloting";
};

export type EdgeUpgrade = {
  upgrade_type: "edge";
};

export type AbilityUpgrade = {
  upgrade_type: "ability";
  ability_name: string;
};

export type PilotUpgradeRequest = SkillUpgrade | EdgeUpgrade | AbilityUpgrade;
</file>

<file path="frontend/src/App.css">
.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero {
  position: relative;

  .base,
  .framework,
  .vite {
    inset-inline: 0;
    margin: 0 auto;
  }

  .base {
    width: 170px;
    position: relative;
    z-index: 0;
  }

  .framework,
  .vite {
    position: absolute;
  }

  .framework {
    z-index: 1;
    top: 34px;
    height: 28px;
    transform: perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg)
      scale(1.4);
  }

  .vite {
    z-index: 0;
    top: 107px;
    height: 26px;
    width: auto;
    transform: perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg)
      scale(0.8);
  }
}

#center {
  display: flex;
  flex-direction: column;
  gap: 25px;
  place-content: center;
  place-items: center;
  flex-grow: 1;

  @media (max-width: 1024px) {
    padding: 32px 20px 24px;
    gap: 18px;
  }
}

#next-steps {
  display: flex;
  border-top: 1px solid var(--border);
  text-align: left;

  & > div {
    flex: 1 1 0;
    padding: 32px;
    @media (max-width: 1024px) {
      padding: 24px 20px;
    }
  }

  .icon {
    margin-bottom: 16px;
    width: 22px;
    height: 22px;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    text-align: center;
  }
}

#docs {
  border-right: 1px solid var(--border);

  @media (max-width: 1024px) {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}

#next-steps ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 32px 0 0;

  .logo {
    height: 18px;
  }

  a {
    color: var(--text-h);
    font-size: 16px;
    border-radius: 6px;
    background: var(--social-bg);
    display: flex;
    padding: 6px 12px;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: var(--shadow);
    }
    .button-icon {
      height: 18px;
      width: 18px;
    }
  }

  @media (max-width: 1024px) {
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;

    li {
      flex: 1 1 calc(50% - 8px);
    }

    a {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }
}

#spacer {
  height: 88px;
  border-top: 1px solid var(--border);
  @media (max-width: 1024px) {
    height: 48px;
  }
}

.ticks {
  position: relative;
  width: 100%;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: -4.5px;
    border: 5px solid transparent;
  }

  &::before {
    left: 0;
    border-left-color: var(--border);
  }
  &::after {
    right: 0;
    border-right-color: var(--border);
  }
}
</file>

<file path="frontend/src/App.tsx">
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { LoginPage } from './pages/Auth/LoginPage';
import { RegisterPage } from './pages/Auth/RegisterPage';
import { ForceCreationPage } from './pages/ForceWizard/ForceCreationPage';
import { DashboardPage } from './pages/Dashboard/DashboardPage';
import { ForceSelectionPage } from './pages/ForceSelection/ForceSelectionPage';
import { PilotProgressionPage } from './pages/Pilot/PilotProgressionPage';

const queryClient = new QueryClient();

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Защищенные маршруты */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<ForceSelectionPage />} />
            <Route path="/forces/create" element={<ForceCreationPage />} />
            <Route path="/forces/:id" element={<DashboardPage />} />
            <Route path="/pilots/:id" element={<PilotProgressionPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
</file>

<file path="frontend/src/index.css">
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --text: #6b6375;
  --text-h: #08060d;
  --bg: #fff;
  --border: #e5e4e7;
  --code-bg: #f4f3ec;
  --accent: #aa3bff;
  --accent-bg: rgba(170, 59, 255, 0.1);
  --accent-border: rgba(170, 59, 255, 0.5);
  --social-bg: rgba(244, 243, 236, 0.5);
  --shadow:
    rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;

  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, Consolas, monospace;

  font: 18px/145% var(--sans);
  letter-spacing: 0.18px;
  color-scheme: light dark;
  color: var(--text);
  background: var(--bg);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  @media (max-width: 1024px) {
    font-size: 16px;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #9ca3af;
    --text-h: #f3f4f6;
    --bg: #16171d;
    --border: #2e303a;
    --code-bg: #1f2028;
    --accent: #c084fc;
    --accent-bg: rgba(192, 132, 252, 0.15);
    --accent-border: rgba(192, 132, 252, 0.5);
    --social-bg: rgba(47, 48, 58, 0.5);
    --shadow:
      rgba(0, 0, 0, 0.4) 0 10px 15px -3px, rgba(0, 0, 0, 0.25) 0 4px 6px -2px;
  }

  #social .button-icon {
    filter: invert(1) brightness(2);
  }
}

#root {
  width: 1126px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  border-inline: 1px solid var(--border);
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

body {
  margin: 0;
}

h1,
h2 {
  font-family: var(--heading);
  font-weight: 500;
  color: var(--text-h);
}

h1 {
  font-size: 56px;
  letter-spacing: -1.68px;
  margin: 32px 0;
  @media (max-width: 1024px) {
    font-size: 36px;
    margin: 20px 0;
  }
}
h2 {
  font-size: 24px;
  line-height: 118%;
  letter-spacing: -0.24px;
  margin: 0 0 8px;
  @media (max-width: 1024px) {
    font-size: 20px;
  }
}
p {
  margin: 0;
}

code,
.counter {
  font-family: var(--mono);
  display: inline-flex;
  border-radius: 4px;
  color: var(--text-h);
}

code {
  font-size: 15px;
  line-height: 135%;
  padding: 4px 8px;
  background: var(--code-bg);
}
</file>

<file path="frontend/src/main.tsx">
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
</file>

<file path="frontend/.oxlintrc.json">
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
</file>

<file path="frontend/index.html">
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
</file>

<file path="frontend/package.json">
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "oxlint",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.104.4",
    "axios": "^1.20.0",
    "lucide-react": "^1.59.0",
    "react": "^19.3.1",
    "react-dom": "^19.3.1",
    "react-router-dom": "^7.18.4",
    "zustand": "^5.0.15"
  },
  "devDependencies": {
    "@types/node": "^24.19.2",
    "@types/react": "^19.3.0",
    "@types/react-dom": "^19.3.0",
    "@vitejs/plugin-react": "^6.1.2",
    "autoprefixer": "^10.6.1",
    "oxlint": "^1.88.0",
    "postcss": "^8.5.31",
    "tailwindcss": "^3.4.19",
    "typescript": "~7.0.2",
    "vite": "^8.3.4"
  }
}
</file>

<file path="frontend/postcss.config.js">
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
</file>

<file path="frontend/tailwind.config.js">
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bt: {
          bg: '#0F172A',         // Slate 900
          card: '#1E293B',       // Slate 800
          border: '#334155',     // Slate 700
          amber: '#F59E0B',      // Акцент Warchest / SP
          green: '#10B981',      // Акцент успеха / Операбелен
          red: '#EF4444',        // Критические повреждения / Уничтожен
          blue: '#3B82F6',       // Опыт XP / Пилоты
        }
      }
    },
  },
  plugins: [],
}
</file>

<file path="frontend/tsconfig.app.json">
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023", "DOM"],
    "module": "esnext",
    "types": ["vite/client"],
    "allowArbitraryExtensions": true,
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
</file>

<file path="frontend/tsconfig.json">
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}
</file>

<file path="frontend/tsconfig.node.json">
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023"],
    "types": ["node"],
    "skipLibCheck": true,

    /* Bundler mode */
    "module": "nodenext",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["vite.config.ts"]
}
</file>

<file path="frontend/vite.config.ts">
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
})
</file>

<file path="src/chaos_campaign_api/__init__.py">
def main() -> None:
    print("Hello from chaos-campaign-api!")
</file>

<file path=".python-version">
3.15
</file>

<file path="pytest.ini">
[pytest]
asyncio_mode = auto
testpaths = app/tests
python_files = test_*.py
pythonpath = .
</file>

<file path="app/api/v1/endpoints/tracks.py">
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse
from app.services.track_service import TrackService

router = APIRouter()


@router.post("/{track_id}/start", summary="Старт трека миссии")
async def start_track(
    track_id: str,
    entry_cost_sp: int = Query(100, ge=0),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    return await TrackService.start_track(db=db, force=force, entry_cost_sp=entry_cost_sp)


@router.post("/{track_id}/complete", response_model=TrackCompletionResponse, summary="Подведение итогов миссии")
async def complete_track(
    track_id: str,
    request: TrackCompletionRequest,
    earned_sp: int = Query(150, ge=0),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    return await TrackService.complete_track(
        db=db,
        force=force,
        track_id=track_id,
        earned_sp=earned_sp,
        request=request
    )
</file>

<file path="app/core/exceptions.py">
from fastapi import Request, status
from fastapi.responses import JSONResponse


class ChaosCampaignException(Exception):
    """Базовое исключение бизнес-логики Chaos Campaign."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code


class InsufficientSupportPointsError(Exception):
    """Исключение при нехватке Support Points (SP)."""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        self.message = f"Недостаточно SP: требуется {required}, доступно {available}"
        super().__init__(self.message)

class InvalidStartingForceConfigError(Exception):
    """Исключение при нарушении правил создания стартового отряда."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InsufficientXPError(Exception):
    """Исключение при нехватке XP у пилота."""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        self.message = f"Недостаточно XP: требуется {required}, доступно {available}"
        super().__init__(self.message)

class ReputationRequirementNotMetError(Exception):
    """Исключение при недостаточной репутации для контракта."""
    def __init__(self, required: int, current: int):
        self.required = required
        self.current = current
        self.message = f"Недостаточный уровень репутации: требуется {required}, текущая {current}"
        super().__init__(self.message)


async def chaos_campaign_exception_handler(request: Request, exc: ChaosCampaignException) -> JSONResponse:
    """Глобальный обработчик кастомных ошибок кампании."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": exc.code,
            "message": exc.message,
            "path": request.url.path
        }
    )
</file>

<file path="app/db/models/pilot.py">
import uuid
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class PilotModel(Base):
    __tablename__ = "pilots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    force_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("forces.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gunnery: Mapped[int] = mapped_column(Integer, default=4)
    piloting: Mapped[int] = mapped_column(Integer, default=5)
    
    # Стартовый запас опыта у пилотов — 150 XP
    experience_points: Mapped[int] = mapped_column(Integer, default=150)
    total_xp_earned: Mapped[int] = mapped_column(Integer, default=150)
    
    edge_points: Mapped[int] = mapped_column(Integer, default=1)
    special_abilities: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    is_temporary_hire: Mapped[bool] = mapped_column(Boolean, default=False)

    force: Mapped[Optional["ForceModel"]] = relationship("ForceModel", back_populates="pilots")
</file>

<file path="app/db/models/user.py">
import uuid
from typing import List
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Каскадная связь: при удалении пользователя удаляются его отряды
    forces: Mapped[List["ForceModel"]] = relationship(
        "ForceModel", 
        back_populates="owner", 
        cascade="all, delete"
    )
</file>

<file path="app/schemas/contract.py">
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.force import Faction


class CommandRights(str, Enum):
    INTEGRATED = "Integrated"
    CO_COMMAND = "Co-Command"
    INDEPENDENT = "Independent"


class SalvageRights(str, Enum):
    FULL = "Full"
    SHARED = "Shared"
    EXCHANGE = "Exchange"
    NONE = "None"


class ContractTerms(BaseModel):
    base_payment_sp: int = Field(..., ge=0, description="Базовая выплата в SP")
    overhead_sp: int = Field(..., ge=0, description="Операционные расходы в SP")
    command_rights: CommandRights = CommandRights.INDEPENDENT
    salvage_rights: SalvageRights = SalvageRights.SHARED
    support_rights_percent: int = Field(default=50, ge=0, le=100)
    transport_coverage_percent: int = Field(default=100, ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)


class ContractNegotiationOffer(BaseModel):
    requested_terms: ContractTerms


class ContractResponse(BaseModel):
    id: str
    title: str
    employer: Faction
    target_faction: Faction
    location_hot_spot: str
    required_reputation: int = 1
    terms: ContractTerms
    is_signed: bool = False
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)
</file>

<file path="app/schemas/force.py">
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.schemas.pilot import NamedPilot


class Faction(str, Enum):
    DRACONIS_COMBINE = "Draconis Combine"
    FEDERATED_SUNS = "Federated Suns"
    RAVEN_ALLIANCE = "Raven Alliance"
    CLAN_SEA_FOX = "Clan Sea Fox"
    REPUBLIC_OF_THE_SPHERE = "Republic of the Sphere"
    MERCENARY = "Mercenary"


class UnitStatus(str, Enum):
    OPERATIONAL = "Operational"
    DAMAGED = "Damaged"
    DESTROYED = "Destroyed"
    TRULY_DESTROYED = "Truly Destroyed"


class WeightClass(str, Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    ASSAULT = "Assault"


class MechUnit(BaseModel):
    id: str
    force_id: Optional[str] = None
    chassis: str
    model: str
    tonnage: int
    weight_class: WeightClass
    bv2: int
    status: UnitStatus = UnitStatus.OPERATIONAL
    assigned_pilot_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StartingMechSelection(BaseModel):
    chassis: str
    model: str
    tonnage: int
    weight_class: WeightClass
    bv2: int


class ForceCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    sponsoring_faction: Faction
    starting_pilot_names: List[str] = Field(
        default_factory=lambda: ["Pilot Alpha", "Pilot Bravo"], 
        min_length=2, 
        max_length=2
    )
    selected_mechs: List[StartingMechSelection] = Field(..., min_length=1, max_length=2)

    @model_validator(mode="after")
    def validate_starting_force_rules(self) -> "ForceCreate":
        total_bv = sum(m.bv2 for m in self.selected_mechs)
        if total_bv > 3000:
            raise ValueError(f"Суммарный BV2 выбранных мехов ({total_bv}) превышает максимальный лимит 3000 BV2")
        return self


class ForceResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    sponsoring_faction: Faction
    support_points: int = 3000
    reputation_score: int = 1
    units: List[MechUnit] = []
    pilots: List[NamedPilot] = []

    model_config = ConfigDict(from_attributes=True)


class AssignPilotRequest(BaseModel):
    unit_id: str = Field(..., description="ID меха")
    pilot_id: Optional[str] = Field(None, description="ID пилота (None если снять пилота)")


class StartingFactionOption(BaseModel):
    faction: Faction
    display_name: str
    description: str
    available_rat_mechs: List[StartingMechSelection]


class StartingOptionsResponse(BaseModel):
    available_factions: List[StartingFactionOption]
    max_starting_mechs: int = 2
    max_starting_bv2: int = 3000
    starting_sp: int = 3000
    starting_reputation: int = 1
    starting_pilots_count: int = 2
    starting_xp_per_pilot: int = 150
</file>

<file path="app/schemas/track.py">
from typing import List
from pydantic import BaseModel, Field, model_validator


class PilotTrackPerformance(BaseModel):
    pilot_id: str
    survived: bool = True
    objectives_completed: int = Field(default=0, ge=0)
    kills: int = Field(default=0, ge=0)
    is_mvp: bool = Field(default=False)
    sp_allocated_to_xp: int = Field(default=0, ge=0, le=100)


class TrackCompletionRequest(BaseModel):
    completed_objectives_ids: List[str]
    pilot_performances: List[PilotTrackPerformance]
    damaged_unit_ids: List[str] = []
    destroyed_unit_ids: List[str] = []
    truly_destroyed_unit_ids: List[str] = []

    @model_validator(mode="after")
    def validate_total_sp_conversion(self) -> "TrackCompletionRequest":
        total_sp = sum(p.sp_allocated_to_xp for p in self.pilot_performances)
        if total_sp > 200:
            raise ValueError(f"Суммарная конвертация SP в XP за трек не может превышать 200 SP (запрошено: {total_sp} SP)")
        return self


class XPAllocationResult(BaseModel):
    pilot_id: str
    pilot_name: str
    sp_converted_xp: int
    mvp_bonus_xp: int
    total_xp_gained: int
    new_total_xp: int


class TrackCompletionResponse(BaseModel):
    track_id: str
    sp_earned: int
    total_sp_spent_on_xp: int
    net_sp_gained: int
    xp_allocations: List[XPAllocationResult]
    summary: str
</file>

<file path="app/services/generator_service.py">
import random
from app.schemas.contract import ContractResponse, ContractTerms, CommandRights, SalvageRights
from app.schemas.force import Faction

HOT_SPOTS = ["Alshain", "Buckminster", "Luthien", "Pesht", "Misery"]


class GeneratorService:
    @staticmethod
    def generate_random_contract(
        employer: Faction = Faction.DRACONIS_COMBINE,
        target_faction: Faction = Faction.FEDERATED_SUNS
    ) -> ContractResponse:
        """Процедурная генерация случайного контракта в SP."""
        location = random.choice(HOT_SPOTS)
        base_sp = random.randint(3, 8) * 100
        overhead_sp = random.randint(2, 5) * 100
        req_rep = random.randint(1, 5)

        terms = ContractTerms(
            base_payment_sp=base_sp,
            overhead_sp=overhead_sp,
            command_rights=random.choice(list(CommandRights)),
            salvage_rights=random.choice(list(SalvageRights)),
            support_rights_percent=50,
            transport_coverage_percent=100
        )

        return ContractResponse(
            id="generated-contract-001",
            title=f"Operation at {location}",
            employer=employer,
            target_faction=target_faction,
            location_hot_spot=location,
            required_reputation=req_rep,
            terms=terms,
            is_signed=False,
            is_completed=False
        )
</file>

<file path="app/services/negotiation_engine.py">
from app.db.models.force import ForceModel
from app.schemas.contract import ContractResponse, ContractTerms
from app.core.exceptions import ReputationRequirementNotMetError


class NegotiationEngine:
    @staticmethod
    def validate_negotiation_offer(
        force: ForceModel,
        contract: ContractResponse,
        requested_terms: ContractTerms
    ) -> bool:
        """Сравнивает текущий рейтинг репутации отряда с требуемым уровнем контракта."""
        if force.reputation_score < contract.required_reputation:
            raise ReputationRequirementNotMetError(
                required=contract.required_reputation,
                current=force.reputation_score
            )
        return True
</file>

<file path="app/services/track_service.py">
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InsufficientSupportPointsError
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import UnitStatus
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse, XPAllocationResult


class TrackService:
    @staticmethod
    async def start_track(db: AsyncSession, force: ForceModel, entry_cost_sp: int) -> ForceModel:
        if force.support_points < entry_cost_sp:
            raise InsufficientSupportPointsError(required=entry_cost_sp, available=force.support_points)
        force.support_points -= entry_cost_sp
        db.add(force)
        await db.flush()
        return force

    @staticmethod
    async def complete_track(
        db: AsyncSession,
        force: ForceModel,
        track_id: str,
        earned_sp: int,
        request: TrackCompletionRequest
    ) -> TrackCompletionResponse:
        total_sp_spent = sum(p.sp_allocated_to_xp for p in request.pilot_performances)
        net_sp = earned_sp - total_sp_spent
        
        force.support_points += net_sp
        db.add(force)

        xp_results: List[XPAllocationResult] = []
        for perf in request.pilot_performances:
            pilot_stmt = select(PilotModel).where(PilotModel.id == perf.pilot_id)
            pilot_res = await db.execute(pilot_stmt)
            pilot = pilot_res.scalar_one_or_none()
            
            if pilot:
                sp_xp = perf.sp_allocated_to_xp
                mvp_xp = 50 if perf.is_mvp else 0
                gained_xp = sp_xp + mvp_xp
                
                pilot.experience_points += gained_xp
                pilot.total_xp_earned += gained_xp
                db.add(pilot)

                xp_results.append(
                    XPAllocationResult(
                        pilot_id=pilot.id,
                        pilot_name=pilot.name,
                        sp_converted_xp=sp_xp,
                        mvp_bonus_xp=mvp_xp,
                        total_xp_gained=gained_xp,
                        new_total_xp=pilot.experience_points,
                    )
                )

        if request.damaged_unit_ids:
            await TrackService._update_units_status(db, request.damaged_unit_ids, UnitStatus.DAMAGED)
        if request.destroyed_unit_ids:
            await TrackService._update_units_status(db, request.destroyed_unit_ids, UnitStatus.DESTROYED)
        if request.truly_destroyed_unit_ids:
            await TrackService._update_units_status(db, request.truly_destroyed_unit_ids, UnitStatus.TRULY_DESTROYED)

        await db.flush()

        return TrackCompletionResponse(
            track_id=track_id,
            sp_earned=earned_sp,
            total_sp_spent_on_xp=total_sp_spent,
            net_sp_gained=net_sp,
            xp_allocations=xp_results,
            summary=f"Трек '{track_id}' завершен. Заработано: {earned_sp} SP. Списано на XP: {total_sp_spent} SP. Чистый прирост: {net_sp} SP."
        )

    @staticmethod
    async def _update_units_status(db: AsyncSession, unit_ids: List[str], status: UnitStatus) -> None:
        stmt = select(MechUnitModel).where(MechUnitModel.id.in_(unit_ids))
        res = await db.execute(stmt)
        for unit in res.scalars():
            unit.status = status
            db.add(unit)
</file>

<file path="app/tests/conftest.py">
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.db.database import Base, get_db
from app.db.models.user import UserModel
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import Faction, UnitStatus, WeightClass
from app.core.security import create_access_token, get_password_hash

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    
    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: test_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(test_db: AsyncSession) -> UserModel:
    user = UserModel(username="test_commander", hashed_password=get_password_hash("password123"))
    test_db.add(user)
    await test_db.flush()
    return user


@pytest_asyncio.fixture(scope="function")
async def auth_headers(test_user: UserModel) -> dict:
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def test_force(test_db: AsyncSession, test_user: UserModel) -> ForceModel:
    force = ForceModel(
        owner_id=test_user.id,
        name="Iron Hand Mercenaries",
        sponsoring_faction=Faction.MERCENARY,
        support_points=3000,
        reputation_score=10
    )
    test_db.add(force)
    await test_db.flush()

    pilot_1 = PilotModel(force_id=force.id, name="Pilot Alpha", gunnery=4, piloting=5, experience_points=150)
    pilot_2 = PilotModel(force_id=force.id, name="Pilot Bravo", gunnery=4, piloting=5, experience_points=150)
    test_db.add_all([pilot_1, pilot_2])

    unit = MechUnitModel(
        force_id=force.id,
        chassis="Starslayer",
        model="STY-3C",
        tonnage=50,
        weight_class=WeightClass.MEDIUM,
        bv2=1508,
        status=UnitStatus.OPERATIONAL
    )
    test_db.add(unit)
    await test_db.flush()

    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force.id)
        .options(selectinload(ForceModel.pilots), selectinload(ForceModel.units))
    )
    result = await test_db.execute(stmt)
    return result.scalar_one()
</file>

<file path="app/tests/test_negotiation.py">
import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_negotiate_contract_success(client: AsyncClient, auth_headers: dict, test_force: ForceModel):
    contract_id = "test-contract-001"
    negotiation_payload = {
        "requested_terms": {
            "base_payment_sp": 600,
            "overhead_sp": 250,
            "command_rights": "Independent",
            "salvage_rights": "Shared",
            "support_rights_percent": 50,
            "transport_coverage_percent": 100
        }
    }

    response = await client.post(
        f"{settings.API_V1_STR}/contracts/{contract_id}/negotiate?force_id={test_force.id}",
        json=negotiation_payload,
        headers=auth_headers
    )

    assert response.status_code == 200


async def test_negotiate_contract_insufficient_reputation(client: AsyncClient, auth_headers: dict, test_force: ForceModel, test_db):
    test_force.reputation_score = 0
    test_db.add(test_force)
    await test_db.flush()

    contract_id = "test-contract-002"
    negotiation_payload = {
        "requested_terms": {
            "base_payment_sp": 1000,
            "overhead_sp": 500,
            "command_rights": "Independent",
            "salvage_rights": "Full",
            "support_rights_percent": 100,
            "transport_coverage_percent": 100
        }
    }

    response = await client.post(
        f"{settings.API_V1_STR}/contracts/{contract_id}/negotiate?force_id={test_force.id}",
        json=negotiation_payload,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "REPUTATION_REQUIREMENT_NOT_MET"
</file>

<file path="app/tests/test_pilots.py">
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db.models.force import ForceModel


async def test_upgrade_pilot_gunnery_success(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db: AsyncSession
):
    """Тест успешного улучшения Gunnery с 4 до 3 за 300 XP."""
    pilot = test_force.pilots[0]
    pilot.experience_points = 500  # Добавляем достаточное количество XP (требуется 300 XP)
    test_db.add(pilot)
    await test_db.flush()

    initial_xp = pilot.experience_points

    response = await client.post(
        f"{settings.API_V1_STR}/pilots/{pilot.id}/upgrade",
        json={"upgrade_type": "gunnery"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["gunnery"] == 3
    assert data["experience_points"] == initial_xp - 300


async def test_upgrade_pilot_insufficient_xp(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db: AsyncSession
):
    """Тест ошибки 400 Bad Request при нехватке XP у пилота."""
    pilot = test_force.pilots[0]
    pilot.experience_points = 50  # Устанавливаем заведомо малое значение
    test_db.add(pilot)
    await test_db.flush()

    response = await client.post(
        f"{settings.API_V1_STR}/pilots/{pilot.id}/upgrade",
        json={"upgrade_type": "gunnery"},
        headers=auth_headers
    )

    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "INSUFFICIENT_XP"
</file>

<file path="app/tests/test_tracks.py">
import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_complete_track_transactional_success(client: AsyncClient, auth_headers: dict, test_force: ForceModel):
    pilot = test_force.pilots[0]
    track_id = "track-bravo"
    payload = {
        "completed_objectives_ids": ["obj-primary"],
        "pilot_performances": [
            {
                "pilot_id": pilot.id,
                "survived": True,
                "objectives_completed": 1,
                "kills": 2,
                "is_mvp": True,
                "sp_allocated_to_xp": 80
            }
        ],
        "damaged_unit_ids": []
    }

    response = await client.post(
        f"{settings.API_V1_STR}/tracks/{track_id}/complete?force_id={test_force.id}&earned_sp=400",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["sp_earned"] == 400
    assert data["total_sp_spent_on_xp"] == 80
    assert data["net_sp_gained"] == 320
</file>

<file path="app/config.py">
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Draconis Reach Campaign Manager API"
    VERSION: str = "6.0.0"
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_URL: str = "sqlite+aiosqlite:///./chaos_campaign.db"
    RAT_JSON_PATH: str = "app/db/data/factions_rat.json"

    model_config = ConfigDict(case_sensitive=True)


settings = Settings()
</file>

<file path="frontend/src/api/services.ts">
import api from './client';
import { apiClient } from './client';
import * as T from '../types';
import { Faction } from '../types';

export const authApi = {
  register: (data: { username: string; password: string }) =>
    apiClient.post<{ id: string; username: string }>('/auth/register', data),
  login: (formData: FormData) =>
    apiClient.post<{ access_token: string; token_type: string }>('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
};

export const forcesApi = {
  getStartingOptions: () =>
    apiClient.get<T.StartingOptionsResponse>('/forces/starting-options').then(r => r.data),
  createForce: (data: T.ForceCreate) =>
    apiClient.post<T.ForceResponse>('/forces/', data).then(r => r.data),
  getMyForces: () =>
    apiClient.get<T.ForceResponse[]>('/forces/me').then(r => r.data),
  getForce: (id: string) =>
    apiClient.get<T.ForceResponse>(`/forces/${id}`).then(r => r.data),
  assignPilot: (forceId: string, data: T.AssignPilotRequest) =>
    apiClient.post<T.ForceResponse>(`/forces/${forceId}/assign-pilot`, data).then(r => r.data),
  deleteForce: (forceId: string) =>
    apiClient.delete(`/forces/${forceId}`).then(r => r.data),
  exportRecordSheet: (forceId: string) =>
    apiClient.get(`/forces/${forceId}/export`, { responseType: 'blob' }).then(r => r.data),
};

export const pilotsApi = {
  getPilot: (id: string) =>
    apiClient.get<T.NamedPilot>(`/pilots/${id}`).then((r) => r.data),
  upgradePilot: (id: string, request: T.PilotUpgradeRequest) =>
    apiClient.post<T.NamedPilot>(`/pilots/${id}/upgrade`, request).then((r) => r.data),
};

export enum CommandRights {
  INTEGRATED = 'Integrated',
  CO_COMMAND = 'Co-Command',
  INDEPENDENT = 'Independent',
}

export enum SalvageRights {
  FULL = 'Full',
  SHARED = 'Shared',
  EXCHANGE = 'Exchange',
  NONE = 'None',
}

export interface ContractTerms {
  base_payment_sp: number;
  overhead_sp: number;
  command_rights: CommandRights;
  salvage_rights: SalvageRights;
  support_rights_percent: number;
  transport_coverage_percent: number;
}

export interface ContractResponse {
  id: str;
  title: string;
  employer: Faction;
  target_faction: Faction;
  location_hot_spot: string;
  required_reputation: number;
  terms: ContractTerms;
  is_signed: boolean;
  is_completed: boolean;
}

export interface ContractNegotiationOffer {
  requested_terms: ContractTerms;
}

export const contractsApi = {
  // Получить доступные контракты
  getAvailableContracts: async (params?: { employer?: string; location?: string }): Promise<ContractResponse[]> => {
    const response = await api.get('/contracts/available', { params });
    return response.data;
  },

  // Провести переговоры по изменению условий
  negotiateContract: async (contractId: string, offer: ContractNegotiationOffer): Promise<ContractResponse> => {
    const response = await api.post(`/contracts/${contractId}/negotiate`, offer);
    return response.data;
  },

  // Подписать контракт отрядом
  signContract: async (contractId: string, forceId: string): Promise<ContractResponse> => {
    const response = await api.post(`/contracts/${contractId}/sign`, null, {
      params: { force_id: forceId },
    });
    return response.data;
  },

  // Процедурно сгенерировать новый контракт по правилам Hot Spots
  generateContract: async (): Promise<ContractResponse> => {
    const response = await api.post('/generator/contract');
    return response.data;
  },
};
</file>

<file path="frontend/src/pages/Dashboard/DashboardPage.tsx">
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
  ChevronLeft,
  Sparkles
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
        <button
          onClick={() => setActiveTab('mechs')}
          className={`pb-1 transition-colors border-b-2 ${
            activeTab === 'mechs'
              ? 'text-bt-amber border-bt-amber'
              : 'text-slate-400 hover:text-white border-transparent'
          }`}
        >
          Обзор отряда
        </button>
        <button
          onClick={() => setActiveTab('pilots')}
          className={`pb-1 transition-colors border-b-2 ${
            activeTab === 'pilots'
              ? 'text-bt-amber border-bt-amber'
              : 'text-slate-400 hover:text-white border-transparent'
          }`}
        >
          Прокачка пилотов
        </button>
        <button
          onClick={() => alert("Раздел 'Контракты' появится на Шаге 6")}
          className="text-slate-500 hover:text-slate-400 transition-colors pb-1 border-b-2 border-transparent"
        >
          Контракты
        </button>
        <button
          onClick={() => alert("Раздел 'Миссии' появится на Шаге 7")}
          className="text-slate-500 hover:text-slate-400 transition-colors pb-1 border-b-2 border-transparent"
        >
          Миссии
        </button>
        <button
          onClick={() => alert("Раздел 'Логистика' появится на Шаге 8")}
          className="text-slate-500 hover:text-slate-400 transition-colors pb-1 border-b-2 border-transparent"
        >
          Логистика
        </button>
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
                  className="bg-bt-card border border-bt-border rounded-lg p-5 shadow-lg space-y-4 flex flex-col justify-between"
                >
                  <div className="space-y-4">
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

                    {/* Секция специальных способностей (SPA) */}
                    <div className="bg-slate-900/40 p-2.5 rounded border border-bt-border/40 space-y-1">
                      <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase text-slate-400">
                        <Sparkles className="w-3.5 h-3.5 text-bt-amber" /> Изученные SPA ({pilot.special_abilities?.length || 0}/5):
                      </div>
                      {pilot.special_abilities && pilot.special_abilities.length > 0 ? (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {pilot.special_abilities.map((ability, idx) => (
                            <span
                              key={idx}
                              className="inline-block bg-slate-900 border border-bt-amber/30 text-bt-amber font-mono text-[11px] font-medium px-2 py-0.5 rounded"
                            >
                              {ability}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-xs text-slate-500 italic block pt-0.5">
                          Специальные способности отсутствуют
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-2 border-t border-bt-border/40">
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
</file>

<file path=".gitignore">
# Python files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info
*.pyc
.pytest_cache/
*.db
*.sqlite
*.sqlite3

# Virtual environments
.venv
.env
.db

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
</file>

<file path="pyproject.toml">
[project]
name = "chaos-campaign-api"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.15"
dependencies = [
    "aiosqlite>=0.22.1",
    "alembic>=1.20.0",
    "asyncpg>=0.32.0",
    "fastapi[standard]>=0.143.0",
    "passlib[bcrypt]>=1.7.4",
    "pydantic-settings>=2.15.0",
    "pyjwt>=2.15.1",
    "python-multipart>=0.0.32",
    "sqlalchemy[asyncio]>=2.0.0",
]

[project.scripts]
chaos-campaign-api = "chaos_campaign_api:main"

[build-system]
requires = ["uv_build>=0.13.0,<0.14.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "eralchemy2>=1.4.1",
    "httpx>=0.28.1",
    "pytest>=9.1.1",
    "pytest-asyncio>=1.4.0",
]
</file>

<file path="README.md">
# ⚔️ Chaos Campaign Manager (Draconis Reach)

**Chaos Campaign Manager** — это веб-сервис и REST API для автоматизации ведения наемнических отрядов в настольной стратегической игре **BattleTech Classic** (по правилам *Hot Spots: Draconis Reach* и системе *Chaos Campaign: Mercenaries*).

Сервис берет на себя всю рутину командира: отслеживание состояния боевой техники и пилотов, учет финансово-материальных ресурсов, проведение контрактов, ремонт и утилизацию лома.

---

## 🚀 Основные возможности

* **Архитектура Command Hub (Multi-Force):** Возможность владеть и одновременно управлять несколькими наемническими отрядами в одном аккаунте ($1 \rightarrow N$).


* **Единая экономика Support Points (SP):** Унифицированная финансовая система — покупка и ремонт мехов, вступительные взносы за миссии, оплата контрактов и конвертация в XP рассчитываются строго в SP.


* **Прокачка и управление пилотами:** Нелинейный расчет стоимости улучшения навыков (Gunnery/Piloting), Edge и специальных способностей (SPA).


* **Контракты и переговоры:** Генерация контрактов с учетом репутации отряда, гибкие условия выплат и командных прав.


* **Проведение миссий (Tracks):** Ввод итогов боя, отслеживание потерь/повреждений, распределение XP и наград, а также скрап уничтоженных мехов (возврат 25% стоимости в SP).


* **Логистика и RAT:** Генерация случайного состава техники по таблицам назначения (*Random Assignment Tables — RAT*) выбранной фракции и ремонтный док.


* **Экспорт документов:** Скачивание официальных листов отряда (*Mercenary Force Record Sheet*) в формате JSON.



---

## 🛠 Технологический стек

### Backend

* **Python 3.11+** / **FastAPI**

* **SQLAlchemy 2.0 (Async)** + `asyncpg` / `aiosqlite`

* **Pydantic v2** (DTO с валидацией стартового состава и BV2)


* **Alembic** (управление миграциями БД)


* **OAuth2 + JWT** (аутентификация пользователей)


* **uv** (высокопроизводительный менеджер пакетов Python)



### Frontend

* **React 18** + **Vite**

* **TypeScript 5.0+**

* **TanStack Query v5 (React Query)** + **Zustand 4**

* **Tailwind CSS** + **Radix UI / Shadcn UI**

* **Axios** (с JWT Interceptor)



---

## 📁 Структура проекта

```text
chaos_campaign_api/
├── app/                      # FastAPI Backend приложение[cite: 3, 5]
│   ├── api/v1/               # REST API роутеры (auth, forces, pilots, contracts, tracks, logistics)[cite: 1, 3]
│   ├── core/                 # Безопасность, исключения и логирование[cite: 1, 3]
│   ├── db/                   # Модели SQLAlchemy, сессии и JSON-справочники RAT[cite: 1, 3]
│   ├── schemas/              # Pydantic v2 DTO модели[cite: 1, 3]
│   └── services/             # Бизнес-логика правил BattleTech[cite: 1, 3]
├── frontend/                 # React + TypeScript SPA приложение[cite: 2, 5]
├── alembic/                  # Миграции структуры базы данных[cite: 1, 3]
├── docs/                     # Технические спецификации[cite: 5]
└── pyproject.toml            # Конфигурация проекта и зависимостей[cite: 1, 3, 5]

```

---

## 💻 Быстрый запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/MileshkinMaksim/chaos_campaign_api.git
cd chaos_campaign_api

```

### 2. Запуск Backend (FastAPI)

Проект использует менеджер пакетов `uv`:

```bash
# Установка зависимостей
uv sync

# Применение миграций базы данных
uv run alembic upgrade head

# Запуск веб-сервера разработки
uv run uvicorn app.main:app --reload

```

* **API доступен по адресу:** `http://localhost:8000`
* **Swagger UI документация:** `http://localhost:8000/docs`

### 3. Запуск Frontend (React)

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера Vite
npm run dev

```

* **Интерфейс доступен по адресу:** `http://localhost:5173`

---

## 📡 Основные эндпоинты REST API

| Раздел | Эндпоинт | Метод | Описание |
| --- | --- | --- | --- |
| **Auth** | `/api/v1/auth/register` | `POST` | Регистрация нового командира

 |
| **Auth** | `/api/v1/auth/token` | `POST` | Авторизация и получение JWT-токена

 |
| **Forces** | `/api/v1/forces/me` | `GET` | Получение списка всех отрядов пользователя

 |
| **Forces** | `/api/v1/forces/` | `POST` | Создание нового отряда наемников

 |
| **Forces** | `/api/v1/forces/{id}` | `DELETE` | Каскадное удаление (расформирование) отряда

 |
| **Pilots** | `/api/v1/pilots/{id}/upgrade` | `POST` | Прокачка навыков и очков пилота за XP

 |
| **Contracts** | `/api/v1/contracts/available` | `GET` | Поиск доступных контрактов

 |
| **Tracks** | `/api/v1/tracks/{id}/complete` | `POST` | Завершение миссии, расчет наград и конвертация SP $\rightarrow$ XP

 |
| **Logistics** | `/api/v1/logistics/repair` | `POST` | Ремонт поврежденной техники за SP

 |

---

## 📄 Лицензия

Проект распространяется под лицензией MIT.
</file>

<file path="app/api/v1/endpoints/forces.py">
import json
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import AssignPilotRequest, ForceCreate, ForceResponse
from app.services.force_service import ForceService
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/starting-options", response_model=Dict[str, Any], summary="Получение стартовых опций для создания отряда")
async def get_starting_options():
    """Возвращает список доступных фракций с их описанием и RAT-мехами."""
    default_mechs = [
        {"chassis": "Flea", "model": "FLE-17", "weight_class": "Light", "tonnage": 20, "bv2": 510},
        {"chassis": "Flea", "model": "FLE-21", "weight_class": "Light", "tonnage": 20, "bv2": 826},
        {"chassis": "Chameleon", "model": "CLN-7V", "weight_class": "Medium", "tonnage": 50, "bv2": 1042},
        {"chassis": "Quickdraw", "model": "QKD-5M", "weight_class": "Heavy", "tonnage": 60, "bv2": 1237},
        {"chassis": "Ostsol", "model": "OTL-5M", "weight_class": "Heavy", "tonnage": 60, "bv2": 1245},
        {"chassis": "Chameleon", "model": "CLN-8V", "weight_class": "Medium", "tonnage": 50, "bv2": 1426},
        {"chassis": "Starslayer", "model": "STY-3C", "weight_class": "Medium", "tonnage": 50, "bv2": 1508},
        {"chassis": "Ostsol", "model": "OTL-8E", "weight_class": "Heavy", "tonnage": 60, "bv2": 1552},
        {"chassis": "Caesar", "model": "CES-3R", "weight_class": "Heavy", "tonnage": 70, "bv2": 1578},
        {"chassis": "Caesar", "model": "CES-5R", "weight_class": "Heavy", "tonnage": 70, "bv2": 2192},
        {"chassis": "Starslayer", "model": "STY-4C", "weight_class": "Medium", "tonnage": 50, "bv2": 2218},
        {"chassis": "Quickdraw", "model": "QKD-9G", "weight_class": "Heavy", "tonnage": 60, "bv2": 2224},
        {"chassis": "Devastator", "model": "DVS-2", "weight_class": "Assault", "tonnage": 100, "bv2": 2481},
    ]

    return {
        "available_factions": [
            {
                "faction": "Draconis Combine",
                "display_name": "Draconis Combine",
                "description": "Синдикат Дракона",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Federated Suns",
                "display_name": "Federated Suns",
                "description": "Федеративные Солнца",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Raven Alliance",
                "display_name": "Raven Alliance",
                "description": "Вороний Альянс",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Clan Sea Fox",
                "display_name": "Clan Sea Fox",
                "description": "Клан Морских Лис",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Republic of the Sphere",
                "display_name": "Republic of the Sphere",
                "description": "Республика Сферы",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Mercenary",
                "display_name": "Mercenary",
                "description": "Независимые наемники",
                "available_rat_mechs": default_mechs
            }
        ],
        "max_starting_mechs": 2,
        "max_starting_bv2": 3000,
        "starting_sp": 3000,
        "starting_reputation": 1,
        "starting_pilots_count": 2,
        "starting_xp_per_pilot": 150
    }


@router.get("/me", response_model=List[ForceResponse], summary="Получение всех отрядов текущего пользователя")
async def get_my_forces(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Возвращает список всех отрядов авторизованного пользователя."""
    stmt = (
        select(ForceModel)
        .where(ForceModel.owner_id == current_user.id)
        .options(selectinload(ForceModel.units), selectinload(ForceModel.pilots))
        .order_by(ForceModel.id.desc())
    )
    result = await db.execute(stmt)
    forces = result.scalars().all()

    if not forces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У текущего пользователя еще нет созданного отряда"
        )
    return forces


@router.post("/", response_model=ForceResponse, status_code=status.HTTP_201_CREATED, summary="Создание нового отряда")
async def create_force(
    force_in: ForceCreate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создает новый отряд наемников для авторизованного пользователя."""
    return await ForceService.create_force(db=db, owner_id=current_user.id, force_in=force_in)


@router.get("/{force_id}", response_model=ForceResponse, summary="Получение карточки отряда")
async def get_force(
    force_id: str = Path(..., min_length=3, description="UUID отряда"),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Возвращает полную структуру отряда с подгруженными списками техники и пилотов."""
    return force

@router.delete("/{force_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление отряда")
async def delete_force(
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Каскадно удаляет отряд пользователя со всей связанной техникой и пилотами."""
    await ForceService.delete_force(db=db, force=force)
    return None

@router.post("/{force_id}/assign-pilot", response_model=ForceResponse, summary="Назначение пилота на мех")
async def assign_pilot(
    request: AssignPilotRequest,
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Назначает или снимает пилота с техники в СУБД."""
    try:
        return await ForceService.assign_pilot_to_unit(
            db=db, force=force, unit_id=request.unit_id, pilot_id=request.pilot_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{force_id}/export", summary="Экспорт Mercenary Force Record Sheet")
async def export_force_record_sheet(
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Генерирует и возвращает официальный бланк отряда в формате JSON."""
    record_sheet = {
        "unit_name": force.name,
        "sponsoring_faction": force.sponsoring_faction,
        "warchest_sp": force.support_points,
        "reputation_score": force.reputation_score,
        "total_units_count": len(force.units),
        "total_pilots_count": len(force.pilots),
        "roster": [
            {
                "id": u.id,
                "chassis": u.chassis,
                "model": u.model,
                "tonnage": u.tonnage,
                "weight_class": u.weight_class,
                "bv2": u.bv2,
                "status": u.status,
                "assigned_pilot_id": u.assigned_pilot_id
            } for u in force.units
        ],
        "pilots": [
            {
                "id": p.id,
                "name": p.name,
                "gunnery": p.gunnery,
                "piloting": p.piloting,
                "experience_points": p.experience_points,
                "edge_points": p.edge_points
            } for p in force.pilots
        ]
    }
    return JSONResponse(
        content=jsonable_encoder(record_sheet),
        headers={"Content-Disposition": f"attachment; filename={force.name}_record_sheet.json"}
    )

@router.post("/{force_id}/roster/import", response_model=ForceResponse, summary="Импорт ростера из JSON файла")
async def import_force_roster(
    file: UploadFile = File(...),
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Пакетно загружает список мехов и пилотов из загруженного файла."""
    content = await file.read()
    try:
        data = json.loads(content)
        for unit_data in data.get("units", []):
            unit = MechUnitModel(
                force_id=force.id,
                chassis=unit_data["chassis"],
                model=unit_data["model"],
                tonnage=unit_data["tonnage"],
                weight_class=unit_data["weight_class"],
                bv2=unit_data["bv2"]
            )
            db.add(unit)

        for pilot_data in data.get("pilots", []):
            pilot = PilotModel(
                force_id=force.id,
                name=pilot_data["name"],
                gunnery=pilot_data.get("gunnery", 4),
                piloting=pilot_data.get("piloting", 5)
            )
            db.add(pilot)

        await db.flush()
        return force
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка парсинга файла: {str(e)}")
</file>

<file path="app/db/models/force.py">
import uuid
from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.schemas.force import Faction, UnitStatus, WeightClass


class ForceModel(Base):
    __tablename__ = "forces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sponsoring_faction: Mapped[Faction] = mapped_column(SQLEnum(Faction), nullable=False)
    
    # Единый экономический баланс SP (Warchest) — стартовое значение 3000 SP
    support_points: Mapped[int] = mapped_column(Integer, default=3000, nullable=False)
    
    # Стартовая репутация отряда — значение 1
    reputation_score: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    owner: Mapped["UserModel"] = relationship(
        "UserModel", 
        back_populates="forces"
        )
    units: Mapped[List["MechUnitModel"]] = relationship(
        "MechUnitModel", 
        back_populates="force", 
        cascade="all, delete-orphan"
        )
    pilots: Mapped[List["PilotModel"]] = relationship(
        "PilotModel", 
        back_populates="force", 
        cascade="all, delete-orphan"
        )


class MechUnitModel(Base):
    __tablename__ = "mech_units"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    force_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("forces.id", ondelete="CASCADE"), nullable=True)
    chassis: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    tonnage: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_class: Mapped[WeightClass] = mapped_column(SQLEnum(WeightClass), nullable=False)
    bv2: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[UnitStatus] = mapped_column(SQLEnum(UnitStatus), default=UnitStatus.OPERATIONAL)
    assigned_pilot_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("pilots.id", ondelete="SET NULL"), nullable=True)

    force: Mapped[Optional["ForceModel"]] = relationship(
        "ForceModel", 
        back_populates="units"
        )
</file>

<file path="app/main.py">
import time
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.core.exceptions import (
    InsufficientXPError,
    InsufficientSupportPointsError,
    ReputationRequirementNotMetError,
    InvalidStartingForceConfigError,
)
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(InsufficientXPError)
async def insufficient_xp_handler(request: Request, exc: InsufficientXPError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INSUFFICIENT_XP"}
    )


@app.exception_handler(InsufficientSupportPointsError)
async def insufficient_sp_handler(request: Request, exc: InsufficientSupportPointsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INSUFFICIENT_SUPPORT_POINTS"}
    )


@app.exception_handler(ReputationRequirementNotMetError)
async def reputation_handler(request: Request, exc: ReputationRequirementNotMetError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "REPUTATION_REQUIREMENT_NOT_MET"}
    )


@app.exception_handler(InvalidStartingForceConfigError)
async def invalid_force_handler(request: Request, exc: InvalidStartingForceConfigError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INVALID_STARTING_FORCE_CONFIG"}
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
</file>

<file path="app/services/force_service.py">
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import ForceCreate
from app.core.exceptions import InvalidStartingForceConfigError


class ForceService:
    @staticmethod
    async def create_force(db: AsyncSession, owner_id: str, force_in: ForceCreate) -> ForceModel:
        """Создает новый отряд по правилам спецификации v6.0."""
        if len(force_in.selected_mechs) > 2:
            raise InvalidStartingForceConfigError("Разрешено выбирать не более 2-х стартовых мехов")
        
        total_bv = sum(m.bv2 for m in force_in.selected_mechs)
        if total_bv > 3000:
            raise InvalidStartingForceConfigError(f"Превышен лимит 3000 BV2 (запрошено: {total_bv} BV2)")

        # 1. Инициализация отряда: SP=3000, Rep=1
        force = ForceModel(
            owner_id=owner_id,
            name=force_in.name,
            sponsoring_faction=force_in.sponsoring_faction,
            support_points=3000,
            reputation_score=1
        )
        db.add(force)
        await db.flush()

        # 2. Создание 2-х пилотов с 150 XP
        pilots = []
        for name in force_in.starting_pilot_names:
            pilot = PilotModel(
                force_id=force.id,
                name=name,
                gunnery=4,
                piloting=5,
                experience_points=150,
                total_xp_earned=150
            )
            db.add(pilot)
            pilots.append(pilot)
        await db.flush()

        # 3. Привязка выбранной техники
        for i, mech_data in enumerate(force_in.selected_mechs):
            assigned_pilot = pilots[i].id if i < len(pilots) else None
            unit = MechUnitModel(
                force_id=force.id,
                chassis=mech_data.chassis,
                model=mech_data.model,
                tonnage=mech_data.tonnage,
                weight_class=mech_data.weight_class,
                bv2=mech_data.bv2,
                assigned_pilot_id=assigned_pilot
            )
            db.add(unit)

        await db.commit()

        # 4. Запрос с eager loading связей для безопасной сериализации Pydantic
        stmt = (
            select(ForceModel)
            .where(ForceModel.id == force.id)
            .options(
                selectinload(ForceModel.pilots),
                selectinload(ForceModel.units)
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    create_starting_force = create_force

    @classmethod
    async def assign_pilot_to_unit(
        cls, db: AsyncSession, force: ForceModel, unit_id: str, pilot_id: str | None
    ) -> ForceModel:
        """Назначает или снимает пилота с техники."""
        unit = next((u for u in force.units if u.id == unit_id), None)
        if not unit:
            raise ValueError("Техника не найдена в составе этого отряда")

        if pilot_id:
            pilot = next((p for p in force.pilots if p.id == pilot_id), None)
            if not pilot:
                raise ValueError("Пилот не найден в составе этого отряда")
            unit.assigned_pilot_id = pilot.id
        else:
            unit.assigned_pilot_id = None

        await db.commit()
        await db.refresh(force)
        return force

    @classmethod
    async def delete_force(cls, db: AsyncSession, force: ForceModel) -> None:
        """Каскадно удаляет отряд и все связанные записи (юниты, пилоты)."""
        await db.delete(force)
        await db.commit()
</file>

</files>
````

## File: app/api/v1/endpoints/__init__.py
````python

````

## File: app/api/v1/endpoints/auth.py
````python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.db.models.user import UserModel
from app.schemas.auth import Token, UserRegister, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Регистрация командира")
async def register_user(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрирует нового командира отряда в базе данных.
    
    * **201 Created**: Пользователь успешно создан.
    * **400 Bad Request**: Имя пользователя уже занято.
    """
    stmt = select(UserModel).where(UserModel.username == user_in.username)
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    new_user = UserModel(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(new_user)
    await db.flush()
    return new_user


@router.post("/token", response_model=Token, summary="Получение JWT токена")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентифицирует пользователя по логину/паролю и выдает JWT токен формата Bearer.
    """
    stmt = select(UserModel).where(UserModel.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")
````

## File: app/api/v1/endpoints/contracts.py
````python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.contract import ContractNegotiationOffer, ContractResponse
from app.schemas.force import Faction
from app.services.generator_service import GeneratorService
from app.services.negotiation_engine import NegotiationEngine

router = APIRouter()


@router.get("/available", response_model=List[ContractResponse], summary="Поиск доступных контрактов")
async def get_available_contracts(
    employer: Optional[Faction] = Query(None, description="Фильтр по нанимателю"),
    location: Optional[str] = Query(None, min_length=2, description="Локация Hot Spot"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: UserModel = Depends(get_current_user)
):
    """Возвращает список доступных контрактов с поддержкой фильтрации и пагинации."""
    # Генерация примеров контрактов для каталога
    contracts = [
        GeneratorService.generate_random_contract(
            employer=employer or Faction.DRACONIS_COMBINE,
            target_faction=Faction.FEDERATED_SUNS
        ) for _ in range(limit)
    ]
    return contracts


@router.post("/{contract_id}/negotiate", summary="Переговоры по условиям контракта")
async def negotiate_contract(
    contract_id: str,
    offer: ContractNegotiationOffer,
    force_id: str = Query(..., description="ID отряда"),
    force: ForceModel = Depends(verify_force_ownership)
):
    """
    Проверяет запрашиваемые условия контракта с Очками Репутации отряда.
    
    * **400 Bad Request**: Недостаточно репутации (`ReputationRequirementNotMetError`).
    """
    mock_contract = GeneratorService.generate_random_contract()
    mock_contract.id = contract_id

    NegotiationEngine.validate_negotiation_offer(
        force=force, contract=mock_contract, requested_terms=offer.requested_terms
    )
    mock_contract.terms = offer.requested_terms
    return {"status": "terms_accepted", "contract": mock_contract}


@router.post("/{contract_id}/sign", summary="Подписание контракта")
async def sign_contract(
    contract_id: str,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Подписывает контракт и закрепляет его за отрядом."""
    return {"status": "contract_signed", "contract_id": contract_id, "force_id": force.id}
````

## File: app/api/v1/endpoints/generator.py
````python
from fastapi import APIRouter, Depends
from app.schemas.contract import ContractResponse
from app.schemas.generator import ContractGenerateRequest
from app.services.generator_service import GeneratorService

router = APIRouter()


@router.post("/contract", response_model=ContractResponse, summary="Процедурная генерация контракта")
async def generate_contract(request: ContractGenerateRequest):
    """Создает случайный контракт по правилам книги Hot Spots."""
    return GeneratorService.generate_random_contract(
        employer=request.employer,
        target_faction=request.target_faction
    )
````

## File: app/api/v1/endpoints/logistics.py
````python
import random
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import Faction, WeightClass
from app.schemas.logistics import PurchaseUnitRequest, RepairRequest, ScrapUnitRequest
from app.services.logistics_service import LogisticsService

router = APIRouter()


@router.post("/repair", summary="Ремонт техники за SP")
async def repair_unit(
    request: RepairRequest,
    sp_cost: int = Query(50, ge=0),
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Восстанавливает поврежденный мех до статуса OPERATIONAL за SP."""
    try:
        repaired_unit = await LogisticsService.repair_unit(
            db=db, force=force, unit_id=request.unit_id, sp_cost=sp_cost
        )
        return {"status": "repaired", "unit_id": repaired_unit.id, "remaining_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/scrap", summary="Утилизация уничтоженной техники на лом")
async def scrap_unit(
    request: ScrapUnitRequest,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Списывает полностью уничтоженный мех (TRULY_DESTROYED) и зачисляет 25% стоимости в SP."""
    try:
        sp_yield = await LogisticsService.scrap_unit(db=db, force=force, unit_id=request.unit_id)
        return {"status": "scrapped", "sp_earned": sp_yield, "total_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/buy-unit", summary="Покупка новой техники")
async def buy_unit(
    request: PurchaseUnitRequest,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Приобретает новый мех и привязывает его к ростеру отряда."""
    try:
        new_unit = await LogisticsService.buy_unit(db=db, force=force, request=request)
        return {"status": "purchased", "unit": new_unit, "remaining_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/rat-roll", summary="Ролл по таблицам RAT (Random Assignment Tables)")
async def rat_roll(
    faction: Faction = Query(...),
    weight_class: WeightClass = Query(...),
    unit_rating: str = Query("Scale 1", pattern=r"^Scale [1-3]$")
):
    """Генерирует случайный мех по таблицам RAT региона Draconis Reach."""
    sample_mechs = {
        WeightClass.LIGHT: [("Panther", "PTH-9R"), ("Jenner", "JR7-D"), ("Locust", "LCT-1E")],
        WeightClass.MEDIUM: [("Starslayer", "STAGE-3C"), ("Phoenix Hawk", "PXH-1K"), ("Centurion", "CN9-A")],
        WeightClass.HEAVY: [("Dragon", "DRG-1N"), ("Catapult", "CPLT-C1"), ("Grasshopper", "GHR-5H")],
        WeightClass.ASSAULT: [("Awesome", "AWS-8Q"), ("BattleMaster", "BLR-1D"), ("Stalker", "STK-3H")],
    }
    chassis, model = random.choice(sample_mechs[weight_class])
    return {
        "faction": faction,
        "weight_class": weight_class,
        "unit_rating": unit_rating,
        "rolled_mech": {"chassis": chassis, "model": model}
    }
````

## File: app/api/v1/endpoints/pilots.py
````python
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.schemas.pilot import NamedPilot, PilotUpgradeRequest
from app.services.pilot_service import PilotService

router = APIRouter()


@router.get("/{pilot_id}", response_model=NamedPilot, summary="Информация о пилоте")
async def get_pilot(
    pilot_id: str = Path(..., description="UUID пилота"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Возвращает карточку пилота из СУБД."""
    stmt = select(PilotModel).where(PilotModel.id == pilot_id)
    res = await db.execute(stmt)
    pilot = res.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пилот не найден")
    return pilot


@router.post("/{pilot_id}/upgrade", response_model=NamedPilot, summary="Прокачка пилота за XP")
async def upgrade_pilot(
    request: PilotUpgradeRequest,
    pilot_id: str = Path(..., description="UUID пилота"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Транзакционно улучшает навык Gunnery/Piloting, добавляет Edge или покупает SPA за XP.
    
    * **400 Bad Request**: Недостаточно XP (`InsufficientXPError`) или достигнут предел.
    """
    stmt = select(PilotModel).where(PilotModel.id == pilot_id)
    res = await db.execute(stmt)
    pilot = res.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пилот не найден")

    try:
        return await PilotService.upgrade_pilot(db=db, pilot=pilot, request=request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
````

## File: app/api/v1/__init__.py
````python

````

## File: app/api/v1/api.py
````python
from fastapi import APIRouter
from app.api.v1.endpoints import auth, contracts, forces, generator, logistics, pilots, tracks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(forces.router, prefix="/forces", tags=["Forces"])
api_router.include_router(pilots.router, prefix="/pilots", tags=["Pilots"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
api_router.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])
api_router.include_router(generator.router, prefix="/generator", tags=["Generator"])
````

## File: app/api/__init__.py
````python

````

## File: app/core/__init__.py
````python

````

## File: app/core/security.py
````python
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
import bcrypt
import jwt
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие открытого пароля сохраненному хэшу."""
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """Генерирует хэш bcrypt для пароля с обрезкой до 72 байт."""
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Создает подписанный JWT токен доступа."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "commander_id": str(subject),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
````

## File: app/db/models/__init__.py
````python
from app.db.models.user import UserModel
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel

__all__ = ["UserModel", "ForceModel", "MechUnitModel", "PilotModel"]
````

## File: app/db/__init__.py
````python

````

## File: app/db/database.py
````python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    """Базовый декларативный класс для всех моделей СУБД."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency для инъекции асинхронной сессии базы данных.
    Автоматически фиксирует транзакцию при успехе или откатывает при ошибке.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
````

## File: app/dependencies/__init__.py
````python

````

## File: app/dependencies/auth.py
````python
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.database import get_db
from app.db.models.user import UserModel
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserModel:
    """Извлекает и валидирует текущего пользователя из JWT токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        commander_id: str = payload.get("sub") or payload.get("commander_id")
        if commander_id is None:
            raise credentials_exception
        token_data = TokenData(commander_id=commander_id)
    except jwt.PyJWTError:
        raise credentials_exception

    stmt = select(UserModel).where(UserModel.id == token_data.commander_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Пользователь неактивен"
        )

    return user
````

## File: app/dependencies/campaign.py
````python
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user


async def verify_force_ownership(
    force_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ForceModel:
    """Проверяет существование отряда в СУБД и права доступа текущего пользователя."""
    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force_id)
        .options(
            selectinload(ForceModel.units),
            selectinload(ForceModel.pilots)
        )
    )
    result = await db.execute(stmt)
    force = result.scalar_one_or_none()

    if force is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Отряд с ID '{force_id}' не найден"
        )

    if force.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для управления этим отрядом"
        )

    return force
````

## File: app/dependencies/db.py
````python
from app.db.database import get_db

__all__ = ["get_db"]
````

## File: app/schemas/__init__.py
````python
from app.schemas.auth import Token, TokenData, UserLogin, UserRegister, UserResponse
from app.schemas.pilot import NamedPilot, SkillUpgrade, EdgeUpgrade, AbilityUpgrade, PilotUpgradeRequest
from app.schemas.force import Faction, UnitStatus, WeightClass, MechUnit, ForceCreate, ForceResponse, AssignPilotRequest
from app.schemas.contract import CommandRights, SalvageRights, ContractTerms, ContractNegotiationOffer, ContractResponse
from app.schemas.track import PilotTrackPerformance, TrackCompletionRequest, XPAllocationResult, TrackCompletionResponse
from app.schemas.logistics import RepairRequest, ScrapUnitRequest, PurchaseUnitRequest, RATRollQuery
from app.schemas.generator import ContractGenerateRequest

__all__ = [
    "Token", "TokenData", "UserLogin", "UserRegister", "UserResponse",
    "NamedPilot", "SkillUpgrade", "EdgeUpgrade", "AbilityUpgrade", "PilotUpgradeRequest",
    "Faction", "UnitStatus", "WeightClass", "MechUnit", "ForceCreate", "ForceResponse", "AssignPilotRequest",
    "CommandRights", "SalvageRights", "ContractTerms", "ContractNegotiationOffer", "ContractResponse",
    "PilotTrackPerformance", "TrackCompletionRequest", "XPAllocationResult", "TrackCompletionResponse",
    "RepairRequest", "ScrapUnitRequest", "PurchaseUnitRequest", "RATRollQuery",
    "ContractGenerateRequest",
]
````

## File: app/schemas/auth.py
````python
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Token(BaseModel):
    """Ответ API с JWT токеном доступа."""
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")


class TokenData(BaseModel):
    """Данные, зашифрованные внутри JWT токена."""
    commander_id: Optional[str] = Field(None, description="UUID командира в БД")


class UserLogin(BaseModel):
    """Схема входа пользователя."""
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "commander_vance"})
    password: str = Field(..., min_length=4, json_schema_extra={"example": "strongpassword123"})


class UserRegister(BaseModel):
    """Схема регистрации нового командира в СУБД."""
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "commander_vance"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "strongpassword123"})


class UserResponse(BaseModel):
    """Публичные данные пользователя."""
    id: str = Field(..., description="Уникальный UUID пользователя в БД")
    username: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
````

## File: app/schemas/generator.py
````python
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.force import Faction


class ContractGenerateRequest(BaseModel):
    """Параметры процедуры генерации случайного контракта."""
    employer: Optional[Faction] = Field(None, description="Целевой наниматель")
    target_faction: Optional[Faction] = Field(None, description="Вражеская фракция")
    location_hot_spot: Optional[str] = Field(None, description="Локация в Draconis Reach")
````

## File: app/schemas/logistics.py
````python
from pydantic import BaseModel, Field
from app.schemas.force import Faction, WeightClass


class RepairRequest(BaseModel):
    """Запрос на ремонт поврежденной техники за SP."""
    unit_id: str = Field(..., description="ID поврежденного меха")


class ScrapUnitRequest(BaseModel):
    """Запрос на утилизацию уничтоженной техники (TRULY_DESTROYED) на лом."""
    unit_id: str = Field(..., description="ID техники для утилизации в SP в БД")


class PurchaseUnitRequest(BaseModel):
    """Запрос на покупку новой единицы техники."""
    chassis: str = Field(..., json_schema_extra={"example": "Catapult"})
    model: str = Field(..., json_schema_extra={"example": "CPLT-C1"})
    tonnage: int = Field(..., ge=20, le=100, json_schema_extra={"example": 65})
    weight_class: WeightClass = Field(..., json_schema_extra={"example": WeightClass.HEAVY})
    bv2: int = Field(..., ge=100, le=5000, json_schema_extra={"example": 1399})
    cost_sp: int = Field(..., ge=0, json_schema_extra={"example": 300})


class RATRollQuery(BaseModel):
    """Параметры генерации случайной техники по RAT-таблицам."""
    faction: Faction
    unit_rating: str = Field(..., pattern=r"^Scale [1-3]$", description="Рейтинг подразделения (Scale 1, Scale 2, Scale 3)")
    weight_class: WeightClass
````

## File: app/schemas/pilot.py
````python
from typing import Annotated, List, Literal, Union, Optional
from pydantic import BaseModel, Field, ConfigDict


class NamedPilot(BaseModel):
    """Модель именного пилота отряда наемников."""
    id: str = Field(..., description="Уникальный UUID пилота в БД")
    force_id: Optional[str] = Field(None, description="ID отряда в БД")
    name: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "Maverick Banderas"})
    gunnery: int = Field(default=4, ge=0, le=8, description="Навык стрельбы (чем ниже, тем лучше)")
    piloting: int = Field(default=5, ge=0, le=8, description="Навык пилотирования (чем ниже, тем лучше)")
    
    # Система опыта (XP)
    experience_points: int = Field(default=0, ge=0, description="Доступные очки опыта (XP)")
    total_xp_earned: int = Field(default=0, ge=0, description="Всего заработано XP за кампанию")
    
    # Способности и Edge
    edge_points: int = Field(default=1, ge=0, le=10, description="Текущее значение Edge (0-10)")
    special_abilities: List[str] = Field(
        default_factory=list, 
        json_schema_extra={"example": ["Overcharge", "Dodge", "Marksman"]},
        description="Купленные спец-способности (SPAs) и способности Edge"
    )
    is_temporary_hire: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)


# --- Discriminated Unions для полиморфных запросов на улучшение пилота ---

class SkillUpgrade(BaseModel):
    """Улучшение навыка стрельбы или пилотирования."""
    upgrade_type: Literal["gunnery", "piloting"]


class EdgeUpgrade(BaseModel):
    """Покупка дополнительного очка Edge."""
    upgrade_type: Literal["edge"]


class AbilityUpgrade(BaseModel):
    """Покупка специальной способности (SPA)."""
    upgrade_type: Literal["ability"]
    ability_name: str = Field(..., min_length=2, description="Название спец-способности (SPA)")


PilotUpgradeRequest = Annotated[
    Union[SkillUpgrade, EdgeUpgrade, AbilityUpgrade], 
    Field(discriminator="upgrade_type")
]
````

## File: app/services/__init__.py
````python
from app.services.pilot_service import PilotService
from app.services.negotiation_engine import NegotiationEngine
from app.services.force_service import ForceService
from app.services.track_service import TrackService
from app.services.logistics_service import LogisticsService
from app.services.generator_service import GeneratorService

__all__ = [
    "PilotService",
    "NegotiationEngine",
    "ForceService",
    "TrackService",
    "LogisticsService",
    "GeneratorService",
]
````

## File: app/services/logistics_service.py
````python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.schemas.force import UnitStatus
from app.schemas.logistics import PurchaseUnitRequest


class LogisticsService:
    @staticmethod
    async def repair_unit(db: AsyncSession, force: ForceModel, unit_id: str, sp_cost: int) -> MechUnitModel:
        """Ремонтирует поврежденный мех за SP, возвращая ему статус OPERATIONAL."""
        if force.support_points < sp_cost:
            raise ValueError(f"Недостаточно SP для ремонта. Требуется: {sp_cost}, доступно: {force.support_points}")

        stmt = select(MechUnitModel).where(MechUnitModel.id == unit_id, MechUnitModel.force_id == force.id)
        res = await db.execute(stmt)
        unit = res.scalar_one_or_none()

        if not unit:
            raise ValueError("Техника не найдена в отряде")

        force.support_points -= sp_cost
        unit.status = UnitStatus.OPERATIONAL
        db.add_all([force, unit])
        await db.flush()
        return unit

    @staticmethod
    async def scrap_unit(db: AsyncSession, force: ForceModel, unit_id: str) -> int:
        """
        Утилизирует уничтоженный мех (TRULY_DESTROYED) на лом.
        Зачисляет 25% его базовой стоимости в SP и удаляет объект из БД.
        """
        stmt = select(MechUnitModel).where(MechUnitModel.id == unit_id, MechUnitModel.force_id == force.id)
        res = await db.execute(stmt)
        unit = res.scalar_one_or_none()

        if not unit:
            raise ValueError("Техника не найдена в отряде")
        if unit.status != UnitStatus.TRULY_DESTROYED:
            raise ValueError("На лом можно распилить только полностью уничтоженную технику (TRULY_DESTROYED)")

        # Расчет 25% стоимости от тоннажа/BV2 в SP
        sp_yield = int((unit.tonnage * 10) * 0.25)
        force.support_points += sp_yield

        await db.delete(unit)
        db.add(force)
        await db.flush()
        return sp_yield

    @staticmethod
    async def buy_unit(db: AsyncSession, force: ForceModel, request: PurchaseUnitRequest) -> MechUnitModel:
        """Покупка новой техники за SP."""
        if force.support_points < request.cost_sp:
            raise ValueError(f"Недостаточно SP для покупки. Требуется: {request.cost_sp}, доступно: {force.support_points}")

        force.support_points -= request.cost_sp
        new_unit = MechUnitModel(
            force_id=force.id,
            chassis=request.chassis,
            model=request.model,
            tonnage=request.tonnage,
            weight_class=request.weight_class,
            bv2=request.bv2,
            status=UnitStatus.OPERATIONAL
        )
        db.add_all([force, new_unit])
        await db.flush()
        return new_unit
````

## File: app/services/pilot_service.py
````python
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from app.core.exceptions import InsufficientXPError
from app.db.models.pilot import PilotModel
from app.schemas.pilot import (
    AbilityUpgrade,
    EdgeUpgrade,
    PilotUpgradeRequest,
    SkillUpgrade,
)

# Нелинейные таблицы стоимости прокачки пилотов (в XP) согласно спецификации v3.0
GUNNERY_UPGRADE_COSTS = {4: 300, 3: 700, 2: 1200, 1: 2200}
PILOTING_UPGRADE_COSTS = {5: 100, 4: 200, 3: 700, 2: 1200}
EDGE_UPGRADE_COSTS = {
    1: 60, 2: 120, 3: 200, 4: 300, 5: 420,
    6: 560, 7: 720, 8: 900, 9: 1100
}
SPA_COST_TABLE = [60, 180, 360, 600, 900]


class PilotService:
    @staticmethod
    async def upgrade_pilot(
        db: AsyncSession, 
        pilot: PilotModel, 
        request: PilotUpgradeRequest
    ) -> PilotModel:
        """
        Прокачивает характеристики пилота за XP в рамках асинхронной транзакции БД.
        
        :raises InsufficientXPError: Если у пилота недостаточно experience_points.
        :raises ValueError: Если достигнут лимит развития параметра.
        """
        if isinstance(request, SkillUpgrade):
            if request.upgrade_type == "gunnery":
                cost = GUNNERY_UPGRADE_COSTS.get(pilot.gunnery)
                if cost is None:
                    raise ValueError("Достигнут максимальный навык Gunnery (0)")
                if pilot.experience_points < cost:
                    raise InsufficientXPError(required=cost, available=pilot.experience_points)
                pilot.experience_points -= cost
                pilot.gunnery -= 1

            elif request.upgrade_type == "piloting":
                cost = PILOTING_UPGRADE_COSTS.get(pilot.piloting)
                if cost is None:
                    raise ValueError("Достигнут максимальный навык Piloting (1)")
                if pilot.experience_points < cost:
                    raise InsufficientXPError(required=cost, available=pilot.experience_points)
                pilot.experience_points -= cost
                pilot.piloting -= 1

        elif isinstance(request, EdgeUpgrade):
            cost = EDGE_UPGRADE_COSTS.get(pilot.edge_points)
            if cost is None:
                raise ValueError("Достигнуто максимальное значение Edge (10)")
            if pilot.experience_points < cost:
                raise InsufficientXPError(required=cost, available=pilot.experience_points)
            pilot.experience_points -= cost
            pilot.edge_points += 1

        elif isinstance(request, AbilityUpgrade):
            ability_name = request.ability_name.strip()
            if not ability_name:
                raise ValueError("Название способности не может быть пустым")

            current_abilities = list(getattr(pilot, "special_abilities", []) or [])
            if len(current_abilities) >= 5:
                raise ValueError("Достигнут лимит в 5 специальных способностей")

            if ability_name in current_abilities:
                raise ValueError("Эта способность уже изучена пилотом")

            ability_index = min(len(current_abilities), len(SPA_COST_TABLE) - 1)
            cost = SPA_COST_TABLE[ability_index]

            if pilot.experience_points < cost:
                raise InsufficientXPError(required=cost, available=pilot.experience_points)

            pilot.experience_points -= cost
            current_abilities.append(ability_name)
            pilot.special_abilities = current_abilities
            flag_modified(pilot, "special_abilities")

        db.add(pilot)
        await db.commit()
        await db.refresh(pilot)
        return pilot
````

## File: app/tests/__init__.py
````python

````

## File: app/tests/test_force.py
````python
import pytest
from httpx import AsyncClient
from app.config import settings


async def test_create_force_v6_success(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Iron Hand Mercenaries",
        "sponsoring_faction": "Draconis Combine",
        "starting_pilot_names": ["Kenshin", "Saito"],
        "selected_mechs": [
            {"chassis": "Panther", "model": "PNT-9R", "tonnage": 35, "weight_class": "Light", "bv2": 769},
            {"chassis": "Dragon", "model": "DRG-1N", "tonnage": 60, "weight_class": "Heavy", "bv2": 1125}
        ]
    }

    response = await client.post(f"{settings.API_V1_STR}/forces/", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["support_points"] == 3000
    assert data["reputation_score"] == 1
    assert len(data["pilots"]) == 2
    assert data["pilots"][0]["experience_points"] == 150
    assert len(data["units"]) == 2


async def test_create_force_v6_exceed_bv2_limit(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Heavy Assault Mercs",
        "sponsoring_faction": "Draconis Combine",
        "starting_pilot_names": ["Pilot A", "Pilot B"],
        "selected_mechs": [
            {"chassis": "Atlas", "model": "AS7-D", "tonnage": 100, "weight_class": "Assault", "bv2": 1897},
            {"chassis": "Awesome", "model": "AWS-8Q", "tonnage": 80, "weight_class": "Assault", "bv2": 1605}
        ]  # Итого: 3502 BV2 > 3000 BV2
    }

    response = await client.post(f"{settings.API_V1_STR}/forces/", json=payload, headers=auth_headers)

    assert response.status_code == 422
````

## File: app/__init__.py
````python

````

## File: frontend/src/api/client.ts
````typescript
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
````

## File: frontend/src/components/common/ProtectedRoute.tsx
````typescript
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const ProtectedRoute: React.FC = () => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
````

## File: frontend/src/components/domain/MechStatusBadge.tsx
````typescript
import React from 'react';
import { UnitStatus } from '../../types';

interface MechStatusBadgeProps {
  status: UnitStatus;
}

export const MechStatusBadge: React.FC<MechStatusBadgeProps> = ({ status }) => {
  switch (status) {
    case UnitStatus.OPERATIONAL:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-emerald-950/80 text-emerald-400 border border-emerald-500/40">
          Боеспособен
        </span>
      );
    case UnitStatus.DAMAGED:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-amber-950/80 text-amber-400 border border-amber-500/40">
          Поврежден
        </span>
      );
    case UnitStatus.DESTROYED:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-orange-950/80 text-orange-400 border border-orange-500/40">
          Уничтожен
        </span>
      );
    case UnitStatus.TRULY_DESTROYED:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-red-950/80 text-red-400 border border-red-500/40 animate-pulse">
          Полный лом
        </span>
      );
    default:
      return (
        <span className="px-2.5 py-1 rounded text-xs font-bold uppercase bg-slate-800 text-slate-400">
          {status}
        </span>
      );
  }
};
````

## File: frontend/src/pages/Auth/LoginPage.tsx
````typescript
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
````

## File: frontend/src/pages/Auth/RegisterPage.tsx
````typescript
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authApi } from '../../api/services';
import { Shield, Lock, User as UserIcon } from 'lucide-react';

export const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await authApi.register({ username, password });
      navigate('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
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
            РЕГИСТРАЦИЯ КОМАНДИРА
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
              Имя пользователя / Позывной
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
            {isLoading ? 'Создание записи...' : 'Создать учетную запись'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate-400">
          Уже зарегистрированы?{' '}
          <Link to="/login" className="text-bt-amber hover:underline">
            Войти
          </Link>
        </p>
      </div>
    </div>
  );
};
````

## File: frontend/src/pages/ForceSelection/ForceSelectionPage.tsx
````typescript
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
````

## File: frontend/src/pages/ForceWizard/ForceCreationPage.tsx
````typescript
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
````

## File: frontend/src/store/authStore.ts
````typescript
import { create } from 'zustand';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  setToken: (token) => {
    if (token) {
      localStorage.setItem('token', token);
      set({ token, isAuthenticated: true });
    } else {
      localStorage.removeItem('token');
      set({ token: null, isAuthenticated: false });
    }
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, isAuthenticated: false });
  },
}));
````

## File: frontend/src/types/auth.ts
````typescript
export interface User {
  id: string;
  username: string;
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}
````

## File: frontend/src/types/index.ts
````typescript
export const Faction = {
  DRACONIS_COMBINE: "Draconis Combine",
  FEDERATED_SUNS: "Federated Suns",
  RAVEN_ALLIANCE: "Raven Alliance",
  CLAN_SEA_FOX: "Clan Sea Fox",
  REPUBLIC_OF_THE_SPHERE: "Republic of the Sphere",
  MERCENARY: "Mercenary"
} as const;

export type Faction = (typeof Faction)[keyof typeof Faction];

export const UnitStatus = {
  OPERATIONAL: "Operational",
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  TRULY_DESTROYED: "Truly Destroyed"
} as const;
export type UnitStatus = (typeof UnitStatus)[keyof typeof UnitStatus];

export const WeightClass = {
  LIGHT: "Light",
  MEDIUM: "Medium",
  HEAVY: "Heavy",
  ASSAULT: "Assault"
} as const;
export type WeightClass = (typeof WeightClass)[keyof typeof WeightClass];

export interface NamedPilot {
  id: string;
  force_id?: string | null;
  name: string;
  gunnery: number;
  piloting: number;
  experience_points: number;
  total_xp_earned: number;
  edge_points: number;
  special_abilities: string[];
  is_temporary_hire: boolean;
}

export interface MechUnit {
  id: string;
  force_id?: string | null;
  chassis: string;
  model: string;
  tonnage: number;
  weight_class: WeightClass;
  bv2: number;
  status: UnitStatus;
  assigned_pilot_id?: string | null;
}

export interface StartingMechSelection {
  chassis: string;
  model: string;
  tonnage: number;
  weight_class: WeightClass;
  bv2: number;
}

export interface ForceCreate {
  name: string;
  sponsoring_faction: Faction;
  starting_pilot_names: [string, string];
  selected_mechs: StartingMechSelection[];
}

export interface ForceResponse {
  id: string;
  owner_id: string;
  name: string;
  sponsoring_faction: Faction;
  support_points: number;
  reputation_score: number;
  units: MechUnit[];
  pilots: NamedPilot[];
}

export interface AssignPilotRequest {
  unit_id: string;
  pilot_id?: string | null;
}

export interface StartingFactionOption {
  faction: Faction;
  display_name: string;
  description: string;
  available_rat_mechs: StartingMechSelection[];
}

export interface StartingOptionsResponse {
  available_factions: StartingFactionOption[];
  max_starting_mechs: number;
  max_starting_bv2: number;
  starting_sp: number;
  starting_reputation: number;
  starting_pilots_count: number;
  starting_xp_per_pilot: number;
}

export interface NamedPilot {
  id: string;
  force_id?: string | null;
  name: string;
  gunnery: number; 
  piloting: number; 
  experience_points: number;
  total_xp_earned: number;
  edge_points: number;
  special_abilities: string[];
  is_temporary_hire: boolean;
}

export type SkillUpgrade = {
  upgrade_type: "gunnery" | "piloting";
};

export type EdgeUpgrade = {
  upgrade_type: "edge";
};

export type AbilityUpgrade = {
  upgrade_type: "ability";
  ability_name: string;
};

export type PilotUpgradeRequest = SkillUpgrade | EdgeUpgrade | AbilityUpgrade;
````

## File: frontend/src/App.css
````css
.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero {
  position: relative;

  .base,
  .framework,
  .vite {
    inset-inline: 0;
    margin: 0 auto;
  }

  .base {
    width: 170px;
    position: relative;
    z-index: 0;
  }

  .framework,
  .vite {
    position: absolute;
  }

  .framework {
    z-index: 1;
    top: 34px;
    height: 28px;
    transform: perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg)
      scale(1.4);
  }

  .vite {
    z-index: 0;
    top: 107px;
    height: 26px;
    width: auto;
    transform: perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg)
      scale(0.8);
  }
}

#center {
  display: flex;
  flex-direction: column;
  gap: 25px;
  place-content: center;
  place-items: center;
  flex-grow: 1;

  @media (max-width: 1024px) {
    padding: 32px 20px 24px;
    gap: 18px;
  }
}

#next-steps {
  display: flex;
  border-top: 1px solid var(--border);
  text-align: left;

  & > div {
    flex: 1 1 0;
    padding: 32px;
    @media (max-width: 1024px) {
      padding: 24px 20px;
    }
  }

  .icon {
    margin-bottom: 16px;
    width: 22px;
    height: 22px;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    text-align: center;
  }
}

#docs {
  border-right: 1px solid var(--border);

  @media (max-width: 1024px) {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}

#next-steps ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 32px 0 0;

  .logo {
    height: 18px;
  }

  a {
    color: var(--text-h);
    font-size: 16px;
    border-radius: 6px;
    background: var(--social-bg);
    display: flex;
    padding: 6px 12px;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: var(--shadow);
    }
    .button-icon {
      height: 18px;
      width: 18px;
    }
  }

  @media (max-width: 1024px) {
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;

    li {
      flex: 1 1 calc(50% - 8px);
    }

    a {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }
}

#spacer {
  height: 88px;
  border-top: 1px solid var(--border);
  @media (max-width: 1024px) {
    height: 48px;
  }
}

.ticks {
  position: relative;
  width: 100%;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: -4.5px;
    border: 5px solid transparent;
  }

  &::before {
    left: 0;
    border-left-color: var(--border);
  }
  &::after {
    right: 0;
    border-right-color: var(--border);
  }
}
````

## File: frontend/src/App.tsx
````typescript
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { LoginPage } from './pages/Auth/LoginPage';
import { RegisterPage } from './pages/Auth/RegisterPage';
import { ForceCreationPage } from './pages/ForceWizard/ForceCreationPage';
import { DashboardPage } from './pages/Dashboard/DashboardPage';
import { ForceSelectionPage } from './pages/ForceSelection/ForceSelectionPage';
import { PilotProgressionPage } from './pages/Pilot/PilotProgressionPage';

const queryClient = new QueryClient();

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Защищенные маршруты */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<ForceSelectionPage />} />
            <Route path="/forces/create" element={<ForceCreationPage />} />
            <Route path="/forces/:id" element={<DashboardPage />} />
            <Route path="/pilots/:id" element={<PilotProgressionPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
````

## File: frontend/src/index.css
````css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --text: #6b6375;
  --text-h: #08060d;
  --bg: #fff;
  --border: #e5e4e7;
  --code-bg: #f4f3ec;
  --accent: #aa3bff;
  --accent-bg: rgba(170, 59, 255, 0.1);
  --accent-border: rgba(170, 59, 255, 0.5);
  --social-bg: rgba(244, 243, 236, 0.5);
  --shadow:
    rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;

  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, Consolas, monospace;

  font: 18px/145% var(--sans);
  letter-spacing: 0.18px;
  color-scheme: light dark;
  color: var(--text);
  background: var(--bg);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  @media (max-width: 1024px) {
    font-size: 16px;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #9ca3af;
    --text-h: #f3f4f6;
    --bg: #16171d;
    --border: #2e303a;
    --code-bg: #1f2028;
    --accent: #c084fc;
    --accent-bg: rgba(192, 132, 252, 0.15);
    --accent-border: rgba(192, 132, 252, 0.5);
    --social-bg: rgba(47, 48, 58, 0.5);
    --shadow:
      rgba(0, 0, 0, 0.4) 0 10px 15px -3px, rgba(0, 0, 0, 0.25) 0 4px 6px -2px;
  }

  #social .button-icon {
    filter: invert(1) brightness(2);
  }
}

#root {
  width: 1126px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  border-inline: 1px solid var(--border);
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

body {
  margin: 0;
}

h1,
h2 {
  font-family: var(--heading);
  font-weight: 500;
  color: var(--text-h);
}

h1 {
  font-size: 56px;
  letter-spacing: -1.68px;
  margin: 32px 0;
  @media (max-width: 1024px) {
    font-size: 36px;
    margin: 20px 0;
  }
}
h2 {
  font-size: 24px;
  line-height: 118%;
  letter-spacing: -0.24px;
  margin: 0 0 8px;
  @media (max-width: 1024px) {
    font-size: 20px;
  }
}
p {
  margin: 0;
}

code,
.counter {
  font-family: var(--mono);
  display: inline-flex;
  border-radius: 4px;
  color: var(--text-h);
}

code {
  font-size: 15px;
  line-height: 135%;
  padding: 4px 8px;
  background: var(--code-bg);
}
````

## File: frontend/src/main.tsx
````typescript
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
````

## File: frontend/.oxlintrc.json
````json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
````

## File: frontend/index.html
````html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
````

## File: frontend/package.json
````json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "oxlint",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.104.4",
    "axios": "^1.20.0",
    "lucide-react": "^1.59.0",
    "react": "^19.3.1",
    "react-dom": "^19.3.1",
    "react-router-dom": "^7.18.4",
    "zustand": "^5.0.15"
  },
  "devDependencies": {
    "@types/node": "^24.19.2",
    "@types/react": "^19.3.0",
    "@types/react-dom": "^19.3.0",
    "@vitejs/plugin-react": "^6.1.2",
    "autoprefixer": "^10.6.1",
    "oxlint": "^1.88.0",
    "postcss": "^8.5.31",
    "tailwindcss": "^3.4.19",
    "typescript": "~7.0.2",
    "vite": "^8.3.4"
  }
}
````

## File: frontend/postcss.config.js
````javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
````

## File: frontend/tailwind.config.js
````javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bt: {
          bg: '#0F172A',         // Slate 900
          card: '#1E293B',       // Slate 800
          border: '#334155',     // Slate 700
          amber: '#F59E0B',      // Акцент Warchest / SP
          green: '#10B981',      // Акцент успеха / Операбелен
          red: '#EF4444',        // Критические повреждения / Уничтожен
          blue: '#3B82F6',       // Опыт XP / Пилоты
        }
      }
    },
  },
  plugins: [],
}
````

## File: frontend/tsconfig.app.json
````json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023", "DOM"],
    "module": "esnext",
    "types": ["vite/client"],
    "allowArbitraryExtensions": true,
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
````

## File: frontend/tsconfig.json
````json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}
````

## File: frontend/tsconfig.node.json
````json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023"],
    "types": ["node"],
    "skipLibCheck": true,

    /* Bundler mode */
    "module": "nodenext",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["vite.config.ts"]
}
````

## File: frontend/vite.config.ts
````typescript
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
})
````

## File: src/chaos_campaign_api/__init__.py
````python
def main() -> None:
    print("Hello from chaos-campaign-api!")
````

## File: .python-version
````
3.15
````

## File: pytest.ini
````ini
[pytest]
asyncio_mode = auto
testpaths = app/tests
python_files = test_*.py
pythonpath = .
````

## File: app/api/v1/endpoints/tracks.py
````python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse
from app.services.track_service import TrackService

router = APIRouter()


@router.post("/{track_id}/start", summary="Старт трека миссии")
async def start_track(
    track_id: str,
    entry_cost_sp: int = Query(100, ge=0),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    return await TrackService.start_track(db=db, force=force, entry_cost_sp=entry_cost_sp)


@router.post("/{track_id}/complete", response_model=TrackCompletionResponse, summary="Подведение итогов миссии")
async def complete_track(
    track_id: str,
    request: TrackCompletionRequest,
    earned_sp: int = Query(150, ge=0),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    return await TrackService.complete_track(
        db=db,
        force=force,
        track_id=track_id,
        earned_sp=earned_sp,
        request=request
    )
````

## File: app/core/exceptions.py
````python
from fastapi import Request, status
from fastapi.responses import JSONResponse


class ChaosCampaignException(Exception):
    """Базовое исключение бизнес-логики Chaos Campaign."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code


class InsufficientSupportPointsError(Exception):
    """Исключение при нехватке Support Points (SP)."""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        self.message = f"Недостаточно SP: требуется {required}, доступно {available}"
        super().__init__(self.message)

class InvalidStartingForceConfigError(Exception):
    """Исключение при нарушении правил создания стартового отряда."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InsufficientXPError(Exception):
    """Исключение при нехватке XP у пилота."""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        self.message = f"Недостаточно XP: требуется {required}, доступно {available}"
        super().__init__(self.message)

class ReputationRequirementNotMetError(Exception):
    """Исключение при недостаточной репутации для контракта."""
    def __init__(self, required: int, current: int):
        self.required = required
        self.current = current
        self.message = f"Недостаточный уровень репутации: требуется {required}, текущая {current}"
        super().__init__(self.message)


async def chaos_campaign_exception_handler(request: Request, exc: ChaosCampaignException) -> JSONResponse:
    """Глобальный обработчик кастомных ошибок кампании."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": exc.code,
            "message": exc.message,
            "path": request.url.path
        }
    )
````

## File: app/db/models/pilot.py
````python
import uuid
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class PilotModel(Base):
    __tablename__ = "pilots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    force_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("forces.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gunnery: Mapped[int] = mapped_column(Integer, default=4)
    piloting: Mapped[int] = mapped_column(Integer, default=5)
    
    # Стартовый запас опыта у пилотов — 150 XP
    experience_points: Mapped[int] = mapped_column(Integer, default=150)
    total_xp_earned: Mapped[int] = mapped_column(Integer, default=150)
    
    edge_points: Mapped[int] = mapped_column(Integer, default=1)
    special_abilities: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    is_temporary_hire: Mapped[bool] = mapped_column(Boolean, default=False)

    force: Mapped[Optional["ForceModel"]] = relationship("ForceModel", back_populates="pilots")
````

## File: app/db/models/user.py
````python
import uuid
from typing import List
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Каскадная связь: при удалении пользователя удаляются его отряды
    forces: Mapped[List["ForceModel"]] = relationship(
        "ForceModel", 
        back_populates="owner", 
        cascade="all, delete"
    )
````

## File: app/schemas/contract.py
````python
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.force import Faction


class CommandRights(str, Enum):
    INTEGRATED = "Integrated"
    CO_COMMAND = "Co-Command"
    INDEPENDENT = "Independent"


class SalvageRights(str, Enum):
    FULL = "Full"
    SHARED = "Shared"
    EXCHANGE = "Exchange"
    NONE = "None"


class ContractTerms(BaseModel):
    base_payment_sp: int = Field(..., ge=0, description="Базовая выплата в SP")
    overhead_sp: int = Field(..., ge=0, description="Операционные расходы в SP")
    command_rights: CommandRights = CommandRights.INDEPENDENT
    salvage_rights: SalvageRights = SalvageRights.SHARED
    support_rights_percent: int = Field(default=50, ge=0, le=100)
    transport_coverage_percent: int = Field(default=100, ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)


class ContractNegotiationOffer(BaseModel):
    requested_terms: ContractTerms


class ContractResponse(BaseModel):
    id: str
    title: str
    employer: Faction
    target_faction: Faction
    location_hot_spot: str
    required_reputation: int = 1
    terms: ContractTerms
    is_signed: bool = False
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)
````

## File: app/schemas/force.py
````python
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.schemas.pilot import NamedPilot


class Faction(str, Enum):
    DRACONIS_COMBINE = "Draconis Combine"
    FEDERATED_SUNS = "Federated Suns"
    RAVEN_ALLIANCE = "Raven Alliance"
    CLAN_SEA_FOX = "Clan Sea Fox"
    REPUBLIC_OF_THE_SPHERE = "Republic of the Sphere"
    MERCENARY = "Mercenary"


class UnitStatus(str, Enum):
    OPERATIONAL = "Operational"
    DAMAGED = "Damaged"
    DESTROYED = "Destroyed"
    TRULY_DESTROYED = "Truly Destroyed"


class WeightClass(str, Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    ASSAULT = "Assault"


class MechUnit(BaseModel):
    id: str
    force_id: Optional[str] = None
    chassis: str
    model: str
    tonnage: int
    weight_class: WeightClass
    bv2: int
    status: UnitStatus = UnitStatus.OPERATIONAL
    assigned_pilot_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StartingMechSelection(BaseModel):
    chassis: str
    model: str
    tonnage: int
    weight_class: WeightClass
    bv2: int


class ForceCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    sponsoring_faction: Faction
    starting_pilot_names: List[str] = Field(
        default_factory=lambda: ["Pilot Alpha", "Pilot Bravo"], 
        min_length=2, 
        max_length=2
    )
    selected_mechs: List[StartingMechSelection] = Field(..., min_length=1, max_length=2)

    @model_validator(mode="after")
    def validate_starting_force_rules(self) -> "ForceCreate":
        total_bv = sum(m.bv2 for m in self.selected_mechs)
        if total_bv > 3000:
            raise ValueError(f"Суммарный BV2 выбранных мехов ({total_bv}) превышает максимальный лимит 3000 BV2")
        return self


class ForceResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    sponsoring_faction: Faction
    support_points: int = 3000
    reputation_score: int = 1
    units: List[MechUnit] = []
    pilots: List[NamedPilot] = []

    model_config = ConfigDict(from_attributes=True)


class AssignPilotRequest(BaseModel):
    unit_id: str = Field(..., description="ID меха")
    pilot_id: Optional[str] = Field(None, description="ID пилота (None если снять пилота)")


class StartingFactionOption(BaseModel):
    faction: Faction
    display_name: str
    description: str
    available_rat_mechs: List[StartingMechSelection]


class StartingOptionsResponse(BaseModel):
    available_factions: List[StartingFactionOption]
    max_starting_mechs: int = 2
    max_starting_bv2: int = 3000
    starting_sp: int = 3000
    starting_reputation: int = 1
    starting_pilots_count: int = 2
    starting_xp_per_pilot: int = 150
````

## File: app/schemas/track.py
````python
from typing import List
from pydantic import BaseModel, Field, model_validator


class PilotTrackPerformance(BaseModel):
    pilot_id: str
    survived: bool = True
    objectives_completed: int = Field(default=0, ge=0)
    kills: int = Field(default=0, ge=0)
    is_mvp: bool = Field(default=False)
    sp_allocated_to_xp: int = Field(default=0, ge=0, le=100)


class TrackCompletionRequest(BaseModel):
    completed_objectives_ids: List[str]
    pilot_performances: List[PilotTrackPerformance]
    damaged_unit_ids: List[str] = []
    destroyed_unit_ids: List[str] = []
    truly_destroyed_unit_ids: List[str] = []

    @model_validator(mode="after")
    def validate_total_sp_conversion(self) -> "TrackCompletionRequest":
        total_sp = sum(p.sp_allocated_to_xp for p in self.pilot_performances)
        if total_sp > 200:
            raise ValueError(f"Суммарная конвертация SP в XP за трек не может превышать 200 SP (запрошено: {total_sp} SP)")
        return self


class XPAllocationResult(BaseModel):
    pilot_id: str
    pilot_name: str
    sp_converted_xp: int
    mvp_bonus_xp: int
    total_xp_gained: int
    new_total_xp: int


class TrackCompletionResponse(BaseModel):
    track_id: str
    sp_earned: int
    total_sp_spent_on_xp: int
    net_sp_gained: int
    xp_allocations: List[XPAllocationResult]
    summary: str
````

## File: app/services/generator_service.py
````python
import random
from app.schemas.contract import ContractResponse, ContractTerms, CommandRights, SalvageRights
from app.schemas.force import Faction

HOT_SPOTS = ["Alshain", "Buckminster", "Luthien", "Pesht", "Misery"]


class GeneratorService:
    @staticmethod
    def generate_random_contract(
        employer: Faction = Faction.DRACONIS_COMBINE,
        target_faction: Faction = Faction.FEDERATED_SUNS
    ) -> ContractResponse:
        """Процедурная генерация случайного контракта в SP."""
        location = random.choice(HOT_SPOTS)
        base_sp = random.randint(3, 8) * 100
        overhead_sp = random.randint(2, 5) * 100
        req_rep = random.randint(1, 5)

        terms = ContractTerms(
            base_payment_sp=base_sp,
            overhead_sp=overhead_sp,
            command_rights=random.choice(list(CommandRights)),
            salvage_rights=random.choice(list(SalvageRights)),
            support_rights_percent=50,
            transport_coverage_percent=100
        )

        return ContractResponse(
            id="generated-contract-001",
            title=f"Operation at {location}",
            employer=employer,
            target_faction=target_faction,
            location_hot_spot=location,
            required_reputation=req_rep,
            terms=terms,
            is_signed=False,
            is_completed=False
        )
````

## File: app/services/negotiation_engine.py
````python
from app.db.models.force import ForceModel
from app.schemas.contract import ContractResponse, ContractTerms
from app.core.exceptions import ReputationRequirementNotMetError


class NegotiationEngine:
    @staticmethod
    def validate_negotiation_offer(
        force: ForceModel,
        contract: ContractResponse,
        requested_terms: ContractTerms
    ) -> bool:
        """Сравнивает текущий рейтинг репутации отряда с требуемым уровнем контракта."""
        if force.reputation_score < contract.required_reputation:
            raise ReputationRequirementNotMetError(
                required=contract.required_reputation,
                current=force.reputation_score
            )
        return True
````

## File: app/services/track_service.py
````python
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InsufficientSupportPointsError
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import UnitStatus
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse, XPAllocationResult


class TrackService:
    @staticmethod
    async def start_track(db: AsyncSession, force: ForceModel, entry_cost_sp: int) -> ForceModel:
        if force.support_points < entry_cost_sp:
            raise InsufficientSupportPointsError(required=entry_cost_sp, available=force.support_points)
        force.support_points -= entry_cost_sp
        db.add(force)
        await db.flush()
        return force

    @staticmethod
    async def complete_track(
        db: AsyncSession,
        force: ForceModel,
        track_id: str,
        earned_sp: int,
        request: TrackCompletionRequest
    ) -> TrackCompletionResponse:
        total_sp_spent = sum(p.sp_allocated_to_xp for p in request.pilot_performances)
        net_sp = earned_sp - total_sp_spent
        
        force.support_points += net_sp
        db.add(force)

        xp_results: List[XPAllocationResult] = []
        for perf in request.pilot_performances:
            pilot_stmt = select(PilotModel).where(PilotModel.id == perf.pilot_id)
            pilot_res = await db.execute(pilot_stmt)
            pilot = pilot_res.scalar_one_or_none()
            
            if pilot:
                sp_xp = perf.sp_allocated_to_xp
                mvp_xp = 50 if perf.is_mvp else 0
                gained_xp = sp_xp + mvp_xp
                
                pilot.experience_points += gained_xp
                pilot.total_xp_earned += gained_xp
                db.add(pilot)

                xp_results.append(
                    XPAllocationResult(
                        pilot_id=pilot.id,
                        pilot_name=pilot.name,
                        sp_converted_xp=sp_xp,
                        mvp_bonus_xp=mvp_xp,
                        total_xp_gained=gained_xp,
                        new_total_xp=pilot.experience_points,
                    )
                )

        if request.damaged_unit_ids:
            await TrackService._update_units_status(db, request.damaged_unit_ids, UnitStatus.DAMAGED)
        if request.destroyed_unit_ids:
            await TrackService._update_units_status(db, request.destroyed_unit_ids, UnitStatus.DESTROYED)
        if request.truly_destroyed_unit_ids:
            await TrackService._update_units_status(db, request.truly_destroyed_unit_ids, UnitStatus.TRULY_DESTROYED)

        await db.flush()

        return TrackCompletionResponse(
            track_id=track_id,
            sp_earned=earned_sp,
            total_sp_spent_on_xp=total_sp_spent,
            net_sp_gained=net_sp,
            xp_allocations=xp_results,
            summary=f"Трек '{track_id}' завершен. Заработано: {earned_sp} SP. Списано на XP: {total_sp_spent} SP. Чистый прирост: {net_sp} SP."
        )

    @staticmethod
    async def _update_units_status(db: AsyncSession, unit_ids: List[str], status: UnitStatus) -> None:
        stmt = select(MechUnitModel).where(MechUnitModel.id.in_(unit_ids))
        res = await db.execute(stmt)
        for unit in res.scalars():
            unit.status = status
            db.add(unit)
````

## File: app/tests/conftest.py
````python
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.db.database import Base, get_db
from app.db.models.user import UserModel
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import Faction, UnitStatus, WeightClass
from app.core.security import create_access_token, get_password_hash

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    
    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: test_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(test_db: AsyncSession) -> UserModel:
    user = UserModel(username="test_commander", hashed_password=get_password_hash("password123"))
    test_db.add(user)
    await test_db.flush()
    return user


@pytest_asyncio.fixture(scope="function")
async def auth_headers(test_user: UserModel) -> dict:
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def test_force(test_db: AsyncSession, test_user: UserModel) -> ForceModel:
    force = ForceModel(
        owner_id=test_user.id,
        name="Iron Hand Mercenaries",
        sponsoring_faction=Faction.MERCENARY,
        support_points=3000,
        reputation_score=10
    )
    test_db.add(force)
    await test_db.flush()

    pilot_1 = PilotModel(force_id=force.id, name="Pilot Alpha", gunnery=4, piloting=5, experience_points=150)
    pilot_2 = PilotModel(force_id=force.id, name="Pilot Bravo", gunnery=4, piloting=5, experience_points=150)
    test_db.add_all([pilot_1, pilot_2])

    unit = MechUnitModel(
        force_id=force.id,
        chassis="Starslayer",
        model="STY-3C",
        tonnage=50,
        weight_class=WeightClass.MEDIUM,
        bv2=1508,
        status=UnitStatus.OPERATIONAL
    )
    test_db.add(unit)
    await test_db.flush()

    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force.id)
        .options(selectinload(ForceModel.pilots), selectinload(ForceModel.units))
    )
    result = await test_db.execute(stmt)
    return result.scalar_one()
````

## File: app/tests/test_negotiation.py
````python
import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_negotiate_contract_success(client: AsyncClient, auth_headers: dict, test_force: ForceModel):
    contract_id = "test-contract-001"
    negotiation_payload = {
        "requested_terms": {
            "base_payment_sp": 600,
            "overhead_sp": 250,
            "command_rights": "Independent",
            "salvage_rights": "Shared",
            "support_rights_percent": 50,
            "transport_coverage_percent": 100
        }
    }

    response = await client.post(
        f"{settings.API_V1_STR}/contracts/{contract_id}/negotiate?force_id={test_force.id}",
        json=negotiation_payload,
        headers=auth_headers
    )

    assert response.status_code == 200


async def test_negotiate_contract_insufficient_reputation(client: AsyncClient, auth_headers: dict, test_force: ForceModel, test_db):
    test_force.reputation_score = 0
    test_db.add(test_force)
    await test_db.flush()

    contract_id = "test-contract-002"
    negotiation_payload = {
        "requested_terms": {
            "base_payment_sp": 1000,
            "overhead_sp": 500,
            "command_rights": "Independent",
            "salvage_rights": "Full",
            "support_rights_percent": 100,
            "transport_coverage_percent": 100
        }
    }

    response = await client.post(
        f"{settings.API_V1_STR}/contracts/{contract_id}/negotiate?force_id={test_force.id}",
        json=negotiation_payload,
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "REPUTATION_REQUIREMENT_NOT_MET"
````

## File: app/tests/test_pilots.py
````python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db.models.force import ForceModel


async def test_upgrade_pilot_gunnery_success(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db: AsyncSession
):
    """Тест успешного улучшения Gunnery с 4 до 3 за 300 XP."""
    pilot = test_force.pilots[0]
    pilot.experience_points = 500  # Добавляем достаточное количество XP (требуется 300 XP)
    test_db.add(pilot)
    await test_db.flush()

    initial_xp = pilot.experience_points

    response = await client.post(
        f"{settings.API_V1_STR}/pilots/{pilot.id}/upgrade",
        json={"upgrade_type": "gunnery"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["gunnery"] == 3
    assert data["experience_points"] == initial_xp - 300


async def test_upgrade_pilot_insufficient_xp(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db: AsyncSession
):
    """Тест ошибки 400 Bad Request при нехватке XP у пилота."""
    pilot = test_force.pilots[0]
    pilot.experience_points = 50  # Устанавливаем заведомо малое значение
    test_db.add(pilot)
    await test_db.flush()

    response = await client.post(
        f"{settings.API_V1_STR}/pilots/{pilot.id}/upgrade",
        json={"upgrade_type": "gunnery"},
        headers=auth_headers
    )

    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "INSUFFICIENT_XP"
````

## File: app/tests/test_tracks.py
````python
import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_complete_track_transactional_success(client: AsyncClient, auth_headers: dict, test_force: ForceModel):
    pilot = test_force.pilots[0]
    track_id = "track-bravo"
    payload = {
        "completed_objectives_ids": ["obj-primary"],
        "pilot_performances": [
            {
                "pilot_id": pilot.id,
                "survived": True,
                "objectives_completed": 1,
                "kills": 2,
                "is_mvp": True,
                "sp_allocated_to_xp": 80
            }
        ],
        "damaged_unit_ids": []
    }

    response = await client.post(
        f"{settings.API_V1_STR}/tracks/{track_id}/complete?force_id={test_force.id}&earned_sp=400",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["sp_earned"] == 400
    assert data["total_sp_spent_on_xp"] == 80
    assert data["net_sp_gained"] == 320
````

## File: app/config.py
````python
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Draconis Reach Campaign Manager API"
    VERSION: str = "6.0.0"
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DATABASE_URL: str = "sqlite+aiosqlite:///./chaos_campaign.db"
    RAT_JSON_PATH: str = "app/db/data/factions_rat.json"

    model_config = ConfigDict(case_sensitive=True)


settings = Settings()
````

## File: frontend/src/api/services.ts
````typescript
import { apiClient } from './client';
import * as T from '../types';
import { Faction } from '../types';

export const authApi = {
  register: (data: { username: string; password: string }) =>
    apiClient.post<{ id: string; username: string }>('/auth/register', data),
  login: (formData: FormData) =>
    apiClient.post<{ access_token: string; token_type: string }>('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
};

export const forcesApi = {
  getStartingOptions: () =>
    apiClient.get<T.StartingOptionsResponse>('/forces/starting-options').then(r => r.data),
  createForce: (data: T.ForceCreate) =>
    apiClient.post<T.ForceResponse>('/forces/', data).then(r => r.data),
  getMyForces: () =>
    apiClient.get<T.ForceResponse[]>('/forces/me').then(r => r.data),
  getForce: (id: string) =>
    apiClient.get<T.ForceResponse>(`/forces/${id}`).then(r => r.data),
  assignPilot: (forceId: string, data: T.AssignPilotRequest) =>
    apiClient.post<T.ForceResponse>(`/forces/${forceId}/assign-pilot`, data).then(r => r.data),
  deleteForce: (forceId: string) =>
    apiClient.delete(`/forces/${forceId}`).then(r => r.data),
  exportRecordSheet: (forceId: string) =>
    apiClient.get(`/forces/${forceId}/export`, { responseType: 'blob' }).then(r => r.data),
};

export const pilotsApi = {
  getPilot: (id: string) =>
    apiClient.get<T.NamedPilot>(`/pilots/${id}`).then((r) => r.data),
  upgradePilot: (id: string, request: T.PilotUpgradeRequest) =>
    apiClient.post<T.NamedPilot>(`/pilots/${id}/upgrade`, request).then((r) => r.data),
};

export enum CommandRights {
  INTEGRATED = 'Integrated',
  CO_COMMAND = 'Co-Command',
  INDEPENDENT = 'Independent',
}

export enum SalvageRights {
  FULL = 'Full',
  SHARED = 'Shared',
  EXCHANGE = 'Exchange',
  NONE = 'None',
}

export interface ContractTerms {
  base_payment_sp: number;
  overhead_sp: number;
  command_rights: CommandRights;
  salvage_rights: SalvageRights;
  support_rights_percent: number;
  transport_coverage_percent: number;
}

export interface ContractResponse {
  id: string;
  title: string;
  employer: Faction;
  target_faction: Faction;
  location_hot_spot: string;
  required_reputation: number;
  terms: ContractTerms;
  is_signed: boolean;
  is_completed: boolean;
}

export interface ContractNegotiationOffer {
  requested_terms: ContractTerms;
}

export const contractsApi = {
  // Получить доступные контракты
  getAvailableContracts: async (params?: { employer?: string; location?: string }): Promise<ContractResponse[]> => {
    const response = await apiClient.get('/contracts/available', { params });
    return response.data;
  },

  // Провести переговоры по изменению условий
  negotiateContract: async (contractId: string, offer: ContractNegotiationOffer): Promise<ContractResponse> => {
    const response = await apiClient.post(`/contracts/${contractId}/negotiate`, offer);
    return response.data;
  },

  // Подписать контракт отрядом
  signContract: async (contractId: string, forceId: string): Promise<ContractResponse> => {
    const response = await apiClient.post(`/contracts/${contractId}/sign`, null, {
      params: { force_id: forceId },
    });
    return response.data;
  },

  // Процедурно сгенерировать новый контракт по правилам Hot Spots
  generateContract: async (): Promise<ContractResponse> => {
    const response = await apiClient.post('/generator/contract');
    return response.data;
  },
};
````

## File: frontend/src/pages/Dashboard/DashboardPage.tsx
````typescript
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
  ChevronLeft,
  Sparkles
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
        <button
          onClick={() => setActiveTab('mechs')}
          className={`pb-1 transition-colors border-b-2 ${
            activeTab === 'mechs'
              ? 'text-bt-amber border-bt-amber'
              : 'text-slate-400 hover:text-white border-transparent'
          }`}
        >
          Обзор отряда
        </button>
        <button
          onClick={() => setActiveTab('pilots')}
          className={`pb-1 transition-colors border-b-2 ${
            activeTab === 'pilots'
              ? 'text-bt-amber border-bt-amber'
              : 'text-slate-400 hover:text-white border-transparent'
          }`}
        >
          Прокачка пилотов
        </button>
        <button
          onClick={() => alert("Раздел 'Контракты' появится на Шаге 6")}
          className="text-slate-500 hover:text-slate-400 transition-colors pb-1 border-b-2 border-transparent"
        >
          Контракты
        </button>
        <button
          onClick={() => alert("Раздел 'Миссии' появится на Шаге 7")}
          className="text-slate-500 hover:text-slate-400 transition-colors pb-1 border-b-2 border-transparent"
        >
          Миссии
        </button>
        <button
          onClick={() => alert("Раздел 'Логистика' появится на Шаге 8")}
          className="text-slate-500 hover:text-slate-400 transition-colors pb-1 border-b-2 border-transparent"
        >
          Логистика
        </button>
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
                  className="bg-bt-card border border-bt-border rounded-lg p-5 shadow-lg space-y-4 flex flex-col justify-between"
                >
                  <div className="space-y-4">
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

                    {/* Секция специальных способностей (SPA) */}
                    <div className="bg-slate-900/40 p-2.5 rounded border border-bt-border/40 space-y-1">
                      <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase text-slate-400">
                        <Sparkles className="w-3.5 h-3.5 text-bt-amber" /> Изученные SPA ({pilot.special_abilities?.length || 0}/5):
                      </div>
                      {pilot.special_abilities && pilot.special_abilities.length > 0 ? (
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {pilot.special_abilities.map((ability, idx) => (
                            <span
                              key={idx}
                              className="inline-block bg-slate-900 border border-bt-amber/30 text-bt-amber font-mono text-[11px] font-medium px-2 py-0.5 rounded"
                            >
                              {ability}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-xs text-slate-500 italic block pt-0.5">
                          Специальные способности отсутствуют
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-2 border-t border-bt-border/40">
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
````

## File: .gitignore
````
# Python files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info
*.pyc
.pytest_cache/
*.db
*.sqlite
*.sqlite3

# Virtual environments
.venv
.env
.db

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
````

## File: pyproject.toml
````toml
[project]
name = "chaos-campaign-api"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.15"
dependencies = [
    "aiosqlite>=0.22.1",
    "alembic>=1.20.0",
    "asyncpg>=0.32.0",
    "fastapi[standard]>=0.143.0",
    "passlib[bcrypt]>=1.7.4",
    "pydantic-settings>=2.15.0",
    "pyjwt>=2.15.1",
    "python-multipart>=0.0.32",
    "sqlalchemy[asyncio]>=2.0.0",
]

[project.scripts]
chaos-campaign-api = "chaos_campaign_api:main"

[build-system]
requires = ["uv_build>=0.13.0,<0.14.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "eralchemy2>=1.4.1",
    "httpx>=0.28.1",
    "pytest>=9.1.1",
    "pytest-asyncio>=1.4.0",
]

[tool.uv]
package = false
````

## File: README.md
````markdown
# ⚔️ Chaos Campaign Manager (Draconis Reach)

**Chaos Campaign Manager** — это веб-сервис и REST API для автоматизации ведения наемнических отрядов в настольной стратегической игре **BattleTech Classic** (по правилам *Hot Spots: Draconis Reach* и системе *Chaos Campaign: Mercenaries*).

Сервис берет на себя всю рутину командира: отслеживание состояния боевой техники и пилотов, учет финансово-материальных ресурсов, проведение контрактов, ремонт и утилизацию лома.

---

## 🚀 Основные возможности

* **Архитектура Command Hub (Multi-Force):** Возможность владеть и одновременно управлять несколькими наемническими отрядами в одном аккаунте ($1 \rightarrow N$).


* **Единая экономика Support Points (SP):** Унифицированная финансовая система — покупка и ремонт мехов, вступительные взносы за миссии, оплата контрактов и конвертация в XP рассчитываются строго в SP.


* **Прокачка и управление пилотами:** Нелинейный расчет стоимости улучшения навыков (Gunnery/Piloting), Edge и специальных способностей (SPA).


* **Контракты и переговоры:** Генерация контрактов с учетом репутации отряда, гибкие условия выплат и командных прав.


* **Проведение миссий (Tracks):** Ввод итогов боя, отслеживание потерь/повреждений, распределение XP и наград, а также скрап уничтоженных мехов (возврат 25% стоимости в SP).


* **Логистика и RAT:** Генерация случайного состава техники по таблицам назначения (*Random Assignment Tables — RAT*) выбранной фракции и ремонтный док.


* **Экспорт документов:** Скачивание официальных листов отряда (*Mercenary Force Record Sheet*) в формате JSON.



---

## 🛠 Технологический стек

### Backend

* **Python 3.11+** / **FastAPI**

* **SQLAlchemy 2.0 (Async)** + `asyncpg` / `aiosqlite`

* **Pydantic v2** (DTO с валидацией стартового состава и BV2)


* **Alembic** (управление миграциями БД)


* **OAuth2 + JWT** (аутентификация пользователей)


* **uv** (высокопроизводительный менеджер пакетов Python)



### Frontend

* **React 18** + **Vite**

* **TypeScript 5.0+**

* **TanStack Query v5 (React Query)** + **Zustand 4**

* **Tailwind CSS** + **Radix UI / Shadcn UI**

* **Axios** (с JWT Interceptor)



---

## 📁 Структура проекта

```text
chaos_campaign_api/
├── app/                      # FastAPI Backend приложение[cite: 3, 5]
│   ├── api/v1/               # REST API роутеры (auth, forces, pilots, contracts, tracks, logistics)[cite: 1, 3]
│   ├── core/                 # Безопасность, исключения и логирование[cite: 1, 3]
│   ├── db/                   # Модели SQLAlchemy, сессии и JSON-справочники RAT[cite: 1, 3]
│   ├── schemas/              # Pydantic v2 DTO модели[cite: 1, 3]
│   └── services/             # Бизнес-логика правил BattleTech[cite: 1, 3]
├── frontend/                 # React + TypeScript SPA приложение[cite: 2, 5]
├── alembic/                  # Миграции структуры базы данных[cite: 1, 3]
├── docs/                     # Технические спецификации[cite: 5]
└── pyproject.toml            # Конфигурация проекта и зависимостей[cite: 1, 3, 5]

```

---

## 💻 Быстрый запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/MileshkinMaksim/chaos_campaign_api.git
cd chaos_campaign_api

```

### 2. Запуск Backend (FastAPI)

Проект использует менеджер пакетов `uv`:

```bash
# Установка зависимостей
uv sync

# Применение миграций базы данных
uv run alembic upgrade head

# Запуск веб-сервера разработки
uv run uvicorn app.main:app --reload

```

* **API доступен по адресу:** `http://localhost:8000`
* **Swagger UI документация:** `http://localhost:8000/docs`

### 3. Запуск Frontend (React)

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск dev-сервера Vite
npm run dev

```

* **Интерфейс доступен по адресу:** `http://localhost:5173`

---

## 📡 Основные эндпоинты REST API

| Раздел | Эндпоинт | Метод | Описание |
| --- | --- | --- | --- |
| **Auth** | `/api/v1/auth/register` | `POST` | Регистрация нового командира

 |
| **Auth** | `/api/v1/auth/token` | `POST` | Авторизация и получение JWT-токена

 |
| **Forces** | `/api/v1/forces/me` | `GET` | Получение списка всех отрядов пользователя

 |
| **Forces** | `/api/v1/forces/` | `POST` | Создание нового отряда наемников

 |
| **Forces** | `/api/v1/forces/{id}` | `DELETE` | Каскадное удаление (расформирование) отряда

 |
| **Pilots** | `/api/v1/pilots/{id}/upgrade` | `POST` | Прокачка навыков и очков пилота за XP

 |
| **Contracts** | `/api/v1/contracts/available` | `GET` | Поиск доступных контрактов

 |
| **Tracks** | `/api/v1/tracks/{id}/complete` | `POST` | Завершение миссии, расчет наград и конвертация SP $\rightarrow$ XP

 |
| **Logistics** | `/api/v1/logistics/repair` | `POST` | Ремонт поврежденной техники за SP

 |

---

## 📄 Лицензия

Проект распространяется под лицензией MIT.
````

## File: app/api/v1/endpoints/forces.py
````python
import json
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import AssignPilotRequest, ForceCreate, ForceResponse
from app.services.force_service import ForceService
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/starting-options", response_model=Dict[str, Any], summary="Получение стартовых опций для создания отряда")
async def get_starting_options():
    """Возвращает список доступных фракций с их описанием и RAT-мехами."""
    default_mechs = [
        {"chassis": "Flea", "model": "FLE-17", "weight_class": "Light", "tonnage": 20, "bv2": 510},
        {"chassis": "Flea", "model": "FLE-21", "weight_class": "Light", "tonnage": 20, "bv2": 826},
        {"chassis": "Chameleon", "model": "CLN-7V", "weight_class": "Medium", "tonnage": 50, "bv2": 1042},
        {"chassis": "Quickdraw", "model": "QKD-5M", "weight_class": "Heavy", "tonnage": 60, "bv2": 1237},
        {"chassis": "Ostsol", "model": "OTL-5M", "weight_class": "Heavy", "tonnage": 60, "bv2": 1245},
        {"chassis": "Chameleon", "model": "CLN-8V", "weight_class": "Medium", "tonnage": 50, "bv2": 1426},
        {"chassis": "Starslayer", "model": "STY-3C", "weight_class": "Medium", "tonnage": 50, "bv2": 1508},
        {"chassis": "Ostsol", "model": "OTL-8E", "weight_class": "Heavy", "tonnage": 60, "bv2": 1552},
        {"chassis": "Caesar", "model": "CES-3R", "weight_class": "Heavy", "tonnage": 70, "bv2": 1578},
        {"chassis": "Caesar", "model": "CES-5R", "weight_class": "Heavy", "tonnage": 70, "bv2": 2192},
        {"chassis": "Starslayer", "model": "STY-4C", "weight_class": "Medium", "tonnage": 50, "bv2": 2218},
        {"chassis": "Quickdraw", "model": "QKD-9G", "weight_class": "Heavy", "tonnage": 60, "bv2": 2224},
        {"chassis": "Devastator", "model": "DVS-2", "weight_class": "Assault", "tonnage": 100, "bv2": 2481},
    ]

    return {
        "available_factions": [
            {
                "faction": "Draconis Combine",
                "display_name": "Draconis Combine",
                "description": "Синдикат Дракона",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Federated Suns",
                "display_name": "Federated Suns",
                "description": "Федеративные Солнца",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Raven Alliance",
                "display_name": "Raven Alliance",
                "description": "Вороний Альянс",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Clan Sea Fox",
                "display_name": "Clan Sea Fox",
                "description": "Клан Морских Лис",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Republic of the Sphere",
                "display_name": "Republic of the Sphere",
                "description": "Республика Сферы",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Mercenary",
                "display_name": "Mercenary",
                "description": "Независимые наемники",
                "available_rat_mechs": default_mechs
            }
        ],
        "max_starting_mechs": 2,
        "max_starting_bv2": 3000,
        "starting_sp": 3000,
        "starting_reputation": 1,
        "starting_pilots_count": 2,
        "starting_xp_per_pilot": 150
    }


@router.get("/me", response_model=List[ForceResponse], summary="Получение всех отрядов текущего пользователя")
async def get_my_forces(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Возвращает список всех отрядов авторизованного пользователя."""
    stmt = (
        select(ForceModel)
        .where(ForceModel.owner_id == current_user.id)
        .options(selectinload(ForceModel.units), selectinload(ForceModel.pilots))
        .order_by(ForceModel.id.desc())
    )
    result = await db.execute(stmt)
    forces = result.scalars().all()

    if not forces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У текущего пользователя еще нет созданного отряда"
        )
    return forces


@router.post("/", response_model=ForceResponse, status_code=status.HTTP_201_CREATED, summary="Создание нового отряда")
async def create_force(
    force_in: ForceCreate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создает новый отряд наемников для авторизованного пользователя."""
    return await ForceService.create_force(db=db, owner_id=current_user.id, force_in=force_in)


@router.get("/{force_id}", response_model=ForceResponse, summary="Получение карточки отряда")
async def get_force(
    force_id: str = Path(..., min_length=3, description="UUID отряда"),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Возвращает полную структуру отряда с подгруженными списками техники и пилотов."""
    return force

@router.delete("/{force_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление отряда")
async def delete_force(
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Каскадно удаляет отряд пользователя со всей связанной техникой и пилотами."""
    await ForceService.delete_force(db=db, force=force)
    return None

@router.post("/{force_id}/assign-pilot", response_model=ForceResponse, summary="Назначение пилота на мех")
async def assign_pilot(
    request: AssignPilotRequest,
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Назначает или снимает пилота с техники в СУБД."""
    try:
        return await ForceService.assign_pilot_to_unit(
            db=db, force=force, unit_id=request.unit_id, pilot_id=request.pilot_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{force_id}/export", summary="Экспорт Mercenary Force Record Sheet")
async def export_force_record_sheet(
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Генерирует и возвращает официальный бланк отряда в формате JSON."""
    record_sheet = {
        "unit_name": force.name,
        "sponsoring_faction": force.sponsoring_faction,
        "warchest_sp": force.support_points,
        "reputation_score": force.reputation_score,
        "total_units_count": len(force.units),
        "total_pilots_count": len(force.pilots),
        "roster": [
            {
                "id": u.id,
                "chassis": u.chassis,
                "model": u.model,
                "tonnage": u.tonnage,
                "weight_class": u.weight_class,
                "bv2": u.bv2,
                "status": u.status,
                "assigned_pilot_id": u.assigned_pilot_id
            } for u in force.units
        ],
        "pilots": [
            {
                "id": p.id,
                "name": p.name,
                "gunnery": p.gunnery,
                "piloting": p.piloting,
                "experience_points": p.experience_points,
                "edge_points": p.edge_points
            } for p in force.pilots
        ]
    }
    return JSONResponse(
        content=jsonable_encoder(record_sheet),
        headers={"Content-Disposition": f"attachment; filename={force.name}_record_sheet.json"}
    )

@router.post("/{force_id}/roster/import", response_model=ForceResponse, summary="Импорт ростера из JSON файла")
async def import_force_roster(
    file: UploadFile = File(...),
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Пакетно загружает список мехов и пилотов из загруженного файла."""
    content = await file.read()
    try:
        data = json.loads(content)
        for unit_data in data.get("units", []):
            unit = MechUnitModel(
                force_id=force.id,
                chassis=unit_data["chassis"],
                model=unit_data["model"],
                tonnage=unit_data["tonnage"],
                weight_class=unit_data["weight_class"],
                bv2=unit_data["bv2"]
            )
            db.add(unit)

        for pilot_data in data.get("pilots", []):
            pilot = PilotModel(
                force_id=force.id,
                name=pilot_data["name"],
                gunnery=pilot_data.get("gunnery", 4),
                piloting=pilot_data.get("piloting", 5)
            )
            db.add(pilot)

        await db.flush()
        return force
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка парсинга файла: {str(e)}")
````

## File: app/db/models/force.py
````python
import uuid
from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.schemas.force import Faction, UnitStatus, WeightClass


class ForceModel(Base):
    __tablename__ = "forces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sponsoring_faction: Mapped[Faction] = mapped_column(SQLEnum(Faction), nullable=False)
    
    # Единый экономический баланс SP (Warchest) — стартовое значение 3000 SP
    support_points: Mapped[int] = mapped_column(Integer, default=3000, nullable=False)
    
    # Стартовая репутация отряда — значение 1
    reputation_score: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    owner: Mapped["UserModel"] = relationship(
        "UserModel", 
        back_populates="forces"
        )
    units: Mapped[List["MechUnitModel"]] = relationship(
        "MechUnitModel", 
        back_populates="force", 
        cascade="all, delete-orphan"
        )
    pilots: Mapped[List["PilotModel"]] = relationship(
        "PilotModel", 
        back_populates="force", 
        cascade="all, delete-orphan"
        )


class MechUnitModel(Base):
    __tablename__ = "mech_units"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    force_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("forces.id", ondelete="CASCADE"), nullable=True)
    chassis: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    tonnage: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_class: Mapped[WeightClass] = mapped_column(SQLEnum(WeightClass), nullable=False)
    bv2: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[UnitStatus] = mapped_column(SQLEnum(UnitStatus), default=UnitStatus.OPERATIONAL)
    assigned_pilot_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("pilots.id", ondelete="SET NULL"), nullable=True)

    force: Mapped[Optional["ForceModel"]] = relationship(
        "ForceModel", 
        back_populates="units"
        )
````

## File: app/main.py
````python
import time
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.core.exceptions import (
    InsufficientXPError,
    InsufficientSupportPointsError,
    ReputationRequirementNotMetError,
    InvalidStartingForceConfigError,
)
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(InsufficientXPError)
async def insufficient_xp_handler(request: Request, exc: InsufficientXPError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INSUFFICIENT_XP"}
    )


@app.exception_handler(InsufficientSupportPointsError)
async def insufficient_sp_handler(request: Request, exc: InsufficientSupportPointsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INSUFFICIENT_SUPPORT_POINTS"}
    )


@app.exception_handler(ReputationRequirementNotMetError)
async def reputation_handler(request: Request, exc: ReputationRequirementNotMetError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "REPUTATION_REQUIREMENT_NOT_MET"}
    )


@app.exception_handler(InvalidStartingForceConfigError)
async def invalid_force_handler(request: Request, exc: InvalidStartingForceConfigError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INVALID_STARTING_FORCE_CONFIG"}
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
````

## File: app/services/force_service.py
````python
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import ForceCreate
from app.core.exceptions import InvalidStartingForceConfigError


class ForceService:
    @staticmethod
    async def create_force(db: AsyncSession, owner_id: str, force_in: ForceCreate) -> ForceModel:
        """Создает новый отряд по правилам спецификации v6.0."""
        if len(force_in.selected_mechs) > 2:
            raise InvalidStartingForceConfigError("Разрешено выбирать не более 2-х стартовых мехов")
        
        total_bv = sum(m.bv2 for m in force_in.selected_mechs)
        if total_bv > 3000:
            raise InvalidStartingForceConfigError(f"Превышен лимит 3000 BV2 (запрошено: {total_bv} BV2)")

        # 1. Инициализация отряда: SP=3000, Rep=1
        force = ForceModel(
            owner_id=owner_id,
            name=force_in.name,
            sponsoring_faction=force_in.sponsoring_faction,
            support_points=3000,
            reputation_score=1
        )
        db.add(force)
        await db.flush()

        # 2. Создание 2-х пилотов с 150 XP
        pilots = []
        for name in force_in.starting_pilot_names:
            pilot = PilotModel(
                force_id=force.id,
                name=name,
                gunnery=4,
                piloting=5,
                experience_points=150,
                total_xp_earned=150
            )
            db.add(pilot)
            pilots.append(pilot)
        await db.flush()

        # 3. Привязка выбранной техники
        for i, mech_data in enumerate(force_in.selected_mechs):
            assigned_pilot = pilots[i].id if i < len(pilots) else None
            unit = MechUnitModel(
                force_id=force.id,
                chassis=mech_data.chassis,
                model=mech_data.model,
                tonnage=mech_data.tonnage,
                weight_class=mech_data.weight_class,
                bv2=mech_data.bv2,
                assigned_pilot_id=assigned_pilot
            )
            db.add(unit)

        await db.commit()

        # 4. Запрос с eager loading связей для безопасной сериализации Pydantic
        stmt = (
            select(ForceModel)
            .where(ForceModel.id == force.id)
            .options(
                selectinload(ForceModel.pilots),
                selectinload(ForceModel.units)
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    create_starting_force = create_force

    @classmethod
    async def assign_pilot_to_unit(
        cls, db: AsyncSession, force: ForceModel, unit_id: str, pilot_id: str | None
    ) -> ForceModel:
        """Назначает или снимает пилота с техники."""
        unit = next((u for u in force.units if u.id == unit_id), None)
        if not unit:
            raise ValueError("Техника не найдена в составе этого отряда")

        if pilot_id:
            pilot = next((p for p in force.pilots if p.id == pilot_id), None)
            if not pilot:
                raise ValueError("Пилот не найден в составе этого отряда")
            unit.assigned_pilot_id = pilot.id
        else:
            unit.assigned_pilot_id = None

        await db.commit()
        await db.refresh(force)
        return force

    @classmethod
    async def delete_force(cls, db: AsyncSession, force: ForceModel) -> None:
        """Каскадно удаляет отряд и все связанные записи (юниты, пилоты)."""
        await db.delete(force)
        await db.commit()
````
