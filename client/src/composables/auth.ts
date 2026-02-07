import { ref } from 'vue'


const accessToken = ref('')


function getAccessToken() {
    return accessToken.value
}


function setAccessToken(token: string) {
    accessToken.value = token
}


async function refreshAccessToken() {
    try {
        const response = await fetch('http://localhost:8000/api/auth/refresh/', {
            method: 'POST',
            credentials: 'include'
        })

        if(!response.ok) {
            console.error(response.status)
            return false
        }

        const data = await response.json()
        setAccessToken(data.access)
    } catch(err) {
        console.error(err)
        return false
    }

    return true
}


// composable
export function useAuth() {
    return {
        accessToken,
        getAccessToken,
        setAccessToken,
        refreshAccessToken,
    }
}