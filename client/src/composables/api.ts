import { useAuth } from "./auth";


// prevents symbol collision with window.fetch
const api = {
    // wrapper for window.fetch
    //  enforces Authorization: `Bearer ${getAccessToken()}`
    //  enforces credentials: 'include',
    async fetch(input: RequestInfo, init?: RequestInit) {
        const { getAccessToken, refreshAccessToken } = useAuth()

        let headers: HeadersInit = {
            ...(init?.headers || {}),
            Authorization: `Bearer ${getAccessToken()}`,
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