import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

export const api = {
    async request(endpoint: string, options: RequestInit = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        } as HeadersInit;

        if (token) {
            (headers as any)['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers,
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            throw new Error(error.detail || 'An error occurred');
        }

        if (response.status === 204) {
            return null;
        }

        return response.json();
    },

    get(endpoint: string) {
        return this.request(endpoint, { method: 'GET' });
    },

    post(endpoint: string, data: any) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    patch(endpoint: string, data: any) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    },

    delete(endpoint: string) {
        return this.request(endpoint, { method: 'DELETE' });
    },
};
