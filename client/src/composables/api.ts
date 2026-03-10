import { useAuth } from "./auth";


// prevents symbol collision with window.fetch
const api = {
    // wrapper for window.fetch
    //  enforces Authorization: `Bearer ${getAccessToken()}`
    //  enforces credentials: 'include',
    // NOTE: to prevent mishapen authorization headers, bearer 
    // token only added if getAccessToken is not null
    async fetch(input: RequestInfo, init?: RequestInit) {
        const { getAccessToken, refreshAccessToken } = useAuth()

        const token = getAccessToken()
        let headers: HeadersInit = {
            ...(init?.headers || {}),
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
        }

        let response = await fetch(input, {
            ...init,
            headers,
            credentials: 'include',
        })

        // if 401 Unauthorized
        //  attempt token rotation and try again
        if(response.status === 401) {         
            if(!await refreshAccessToken()) {
                return response
            }

            const newToken = getAccessToken()
            headers = {
                ...(init?.headers || {}),
                ...(newToken ? { Authorization: `Bearer ${newToken}` } : {}),
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