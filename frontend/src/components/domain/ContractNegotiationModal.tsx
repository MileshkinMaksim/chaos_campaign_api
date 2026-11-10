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