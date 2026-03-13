import { ref } from 'vue'
import { useAuth } from '@/composables/auth'
import { useApi } from '@/composables/api'

const { isAuthenticated } = useAuth()
const { api } = useApi()

const user = ref<null | {
    first_name: string
    last_name: string
    email: string
    preferred_language: string
    preferred_avatar: number
    type: string
}>(null)

const loading = ref(false)
const error = ref<string | null>(null)

export function useUser() {
    const fetchUser = async (force = true) => {
        if (user.value && !force) return user.value
        loading.value = true
        error.value = null
        try {
            const authenticated = await isAuthenticated()
            if (!authenticated) throw new Error('Not authenticated')
            const response = await api.fetch('/api/account/get_user_info')
            const data = await response.json()
            user.value = data
        } catch (err: any) {
            error.value = err.message
            console.error('Failed to fetch user:', err)
        } finally {
            loading.value = false
        }
        return user.value
    }

    const clearUser = () => {
        user.value = null
    }

    return { user, loading, error, fetchUser, clearUser }
}