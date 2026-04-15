import type { Table } from '@/types/table'

export function parseCSV(text: string): Table {
    const lines = text
        .trim()
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)

    if (!lines[0]) return { headers: [], rows: [] }

    const headers = parseCSVLine(lines[0])
    const rows    = lines.slice(1).map(parseCSVLine)

    return { headers, rows }
}

function parseCSVLine(line: string): string[] {
    const fields: string[] = []
    let i                  = 0

    while (i < line.length) {
        if (line[i] === '"') {
            let field = ''
            i++ // skip opening quote
            
            while (i < line.length) {
                if (line[i] === '"' && line[i + 1] === '"') {
                    field += '"'
                    i += 2
                } else if (line[i] === '"') {
                    i++ // skip closing quote
                    break
                } else {
                    field += line[i++]
                }
            }

            fields.push(field)

            if (line[i] === ',') i++
        } else {
            const end = line.indexOf(',', i)
            
            if (end === -1) {
                fields.push(line.slice(i))
                break
            } else {
                fields.push(line.slice(i, end))
                i = end + 1
            }
        }
    }

    if (line.endsWith(',')) fields.push('')

    return fields
}