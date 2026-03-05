import { ref } from 'vue'
import { useAuth } from '@/composables/auth'

const { getAccessToken, isAuthenticated } = useAuth()

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
            const token = getAccessToken()
            console.log('Token:', token)
            const response = await fetch('/api/account/get_user_info', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            })
            const text = await response.text()
            console.log('Raw response text:', text)
            const data = JSON.parse(text)
            console.log('Raw response data:', data)
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