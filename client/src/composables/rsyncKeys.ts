import { ref } from 'vue'
import { useApi } from '@/composables/api'

export interface RsyncKey {
    id: number
    name: string
    key_type: string
    fingerprint: string
    created_at: string
}

const keys = ref<RsyncKey[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const { api } = useApi()

export function useRsyncKeys() {
    const fetchKeys = async () => {
        loading.value = true
        error.value = null
        try {
            const response = await api.fetch('/api/account/rsync_keys/')
            if (!response.ok) throw new Error(`${response.status}`)
            keys.value = await response.json()
        } catch (e: any) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const createKey = async (name: string, publicKey: string): Promise<RsyncKey> => {
        const response = await api.fetch('/api/account/rsync_keys/create/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, public_key: publicKey }),
        })
        const data = await response.json()
        if (!response.ok) {
            throw new Error(data?.error ?? `${response.status}`)
        }
        await fetchKeys()
        return data
    }

    const deleteKey = async (id: number): Promise<void> => {
        const response = await api.fetch(`/api/account/rsync_keys/${id}/`, { method: 'DELETE' })
        if (!response.ok && response.status !== 204) {
            throw new Error(`${response.status}`)
        }
        await fetchKeys()
    }

    return { keys, loading, error, fetchKeys, createKey, deleteKey }
}
