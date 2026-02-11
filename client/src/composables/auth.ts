import { ref } from 'vue'


const accessToken = ref<string>('')


function getAccessToken() {
    return accessToken.value
}


function setAccessToken(token: string) {
    accessToken.value = token

    return
}


function clearAccessToken() {
    accessToken.value = ''

    return
}


async function refreshAccessToken(): Promise<boolean> {
    try {
        const response = await fetch('http://localhost:8000/api/auth/refresh/', {
            method: 'POST',
            credentials: 'include'
        })

        if(!response.ok) {
            console.error(response.status)
            clearAccessToken()
            
            return false
        }

        const data = await response.json()
        setAccessToken(data.access)
        
        return true
    } catch(err) {
        console.error(err)
        clearAccessToken()
        
        return false
    }
}


async function isAuthenticated(): Promise<boolean> {
    if(accessToken.value) {
        return true
    }
    
    if(await refreshAccessToken()) {
        return true
    }

    clearAccessToken()
    
    return false
}


// composable
export function useAuth() {
    return {
        accessToken,
        getAccessToken,
        setAccessToken,
        refreshAccessToken,
        isAuthenticated,
    }
}