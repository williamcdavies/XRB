import type { DocumentView } from '@/types/view'
import { ref } from 'vue'

const STORAGE_KEY = 'xrb-document-views'

export function useDocumentViews() {
    const views = ref<DocumentView[]>(load())


    function load(): DocumentView[] {
        try {
            const raw = localStorage.getItem(STORAGE_KEY)
            return raw ? JSON.parse(raw) : []
        } catch {
            return []
        }
    }


    function persist() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(views.value))
    }


    function save(view: Omit<DocumentView, 'id' | 'savedAt'>): DocumentView {
        const entry: DocumentView = {
            ...view,
            id:      crypto.randomUUID(),
            savedAt: Date.now(),
        }
        views.value.push(entry)
        persist()
        return entry
    }


    function overwrite(id: string, data: Omit<DocumentView, 'id' | 'savedAt'>): DocumentView | undefined {
        const idx = views.value.findIndex(v => v.id === id)
        if (idx < 0) return undefined

        const updated: DocumentView = {
            ...data,
            id,
            savedAt: Date.now(),
        }
        views.value[idx] = updated
        persist()
        return updated
    }


    function remove(id: string) {
        views.value = views.value.filter(v => v.id !== id)
        persist()
    }


    function get(id: string): DocumentView | undefined {
        return views.value.find(v => v.id === id)
    }


    return { views, save, overwrite, remove, get }
}
