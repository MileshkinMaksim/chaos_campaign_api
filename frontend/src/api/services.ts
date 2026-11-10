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