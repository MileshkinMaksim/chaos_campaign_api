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