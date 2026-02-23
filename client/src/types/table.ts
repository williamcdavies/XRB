export type Table = {
    headers: string[]
    rows:    string[][]
    source?: {
        name: string
        type: string
    }
}