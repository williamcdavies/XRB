import { useAuth } from "./auth";


const { getAccessToken, refreshAccessToken } = useAuth()

const api = {
    // wrapper for window.fetch
    //  enforces Authorization: `Bearer ${getAccessToken()}`
    //  enforces credentials: 'include',
    async fetch(input: RequestInfo, init?: RequestInit) {
        let headers: HeadersInit = {
            ...(init?.headers || {}),
            Authorization: `Bearer ${getAccessToken()}`,
        }

        let response = await fetch(input, {
            ...init,
            headers,
            credentials: 'include',
        })

        // if 401 Unauthorized, attempt to refresh access token and try again
        if(response.status === 401) {
            const token = await refreshAccessToken()
            
            if(!token) {
                return response
            }

            headers =  {
                ...(init?.headers || {}),
                Authorization: `Bearer ${getAccessToken()}`,
            }

            response = await fetch(input, {
                ...init,
                headers,
                credentials: 'include',
            })
        }

        return response
    }
}


// composable
export function useApi() {
    return {
        api,
    }
}