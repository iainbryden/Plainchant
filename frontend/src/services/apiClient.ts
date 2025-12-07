import axios from 'axios';
import type {
  GenerateCantusFirmusRequest,
  GenerateCantusFirmusResponse,
  GenerateCounterpointRequest,
  GenerateCounterpointResponse,
  EvaluateCounterpointRequest,
  EvaluateCounterpointResponse,
  GenerateMultiVoiceRequest,
  GenerateMultiVoiceResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateCantusFirmus = async (
  params: GenerateCantusFirmusRequest
): Promise<GenerateCantusFirmusResponse> => {
  const response = await apiClient.post<GenerateCantusFirmusResponse>(
    '/api/generate-cantus-firmus',
    params
  );
  return response.data;
};

export const generateCounterpoint = async (
  params: GenerateCounterpointRequest
): Promise<GenerateCounterpointResponse> => {
  const response = await apiClient.post<GenerateCounterpointResponse>(
    '/api/generate-counterpoint',
    params
  );
  return response.data;
};

export const evaluateCounterpoint = async (
  params: EvaluateCounterpointRequest
): Promise<EvaluateCounterpointResponse> => {
  const response = await apiClient.post<EvaluateCounterpointResponse>(
    '/api/evaluate-counterpoint',
    params
  );
  return response.data;
};

export const generateMultiVoice = async (
  params: GenerateMultiVoiceRequest
): Promise<GenerateMultiVoiceResponse> => {
  const response = await apiClient.post<GenerateMultiVoiceResponse>(
    '/api/generate-multi-voice',
    params
  );
  return response.data;
};

export const generateSecondSpecies = async (
  params: GenerateCounterpointRequest
): Promise<GenerateCounterpointResponse> => {
  const response = await apiClient.post<GenerateCounterpointResponse>(
    '/api/generate-second-species',
    params
  );
  return response.data;
};

export const generateThirdSpecies = async (
  params: GenerateCounterpointRequest
): Promise<GenerateCounterpointResponse> => {
  const response = await apiClient.post<GenerateCounterpointResponse>(
    '/api/generate-third-species',
    params
  );
  return response.data;
};

export const generateFifthSpecies = async (
  params: GenerateCounterpointRequest
): Promise<GenerateCounterpointResponse> => {
  const response = await apiClient.post<GenerateCounterpointResponse>(
    '/api/generate-fifth-species',
    params
  );
  return response.data;
};

export const checkHealth = async (): Promise<{ status: string }> => {
  const response = await apiClient.get<{ status: string }>('/health');
  return response.data;
};
