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