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
        const response = await fetch('/api/auth/refresh/', {
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


async function googleLogin(): Promise<boolean> {
    return new Promise((resolve) => {
        google.accounts.id.initialize({
            client_id: import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID,
            callback: async (response: google.accounts.id.CredentialResponse) => {
                try {
                    const res = await fetch('/api/auth/google/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ credential: response.credential }),
                        credentials: 'include',
                    })

                    if (!res.ok) {
                        console.error(res.status)
                        resolve(false)
                        return
                    }

                    const data = await res.json()
                    setAccessToken(data.access)
                    resolve(true)
                } catch (err) {
                    console.error(err)
                    resolve(false)
                }
            },
        })
        google.accounts.id.prompt()
    })
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
        googleLogin,
        isAuthenticated,
        clearAccessToken
    }
}