import { apiClient } from './client';
import * as T from '../types';

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
    apiClient.get<Blob>(`/forces/${forceId}/export`, { responseType: 'blob' }).then(r => r.data), // <-- Добавлен .then(r => r.data)
};