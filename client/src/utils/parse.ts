import type { Table } from "@/dgclib/types";


export function parseCSV(text: string): Table {
    const lines = text
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)

    if(!lines[0]) {
        return {
            headers: [],
            rows:    []
        }
    }

    const headers = lines[0].split(',')
    const rows    = lines.slice(1).map(line => line.split(','))

    return { headers, rows }
}