<script setup lang="ts">
    import { computed }          from 'vue'
    import { useRouter }         from 'vue-router'
    import { useDocumentViews }  from '@/composables/views'
    import type { DocumentView } from '@/types/view'


    const router = useRouter()
    const { views, remove: removeView } = useDocumentViews()


    const recentViews = computed(() => {
        return [...views.value].sort((a, b) => {
            const aTime = a.lastAccessedAt ?? a.savedAt
            const bTime = b.lastAccessedAt ?? b.savedAt
            return bTime - aTime
        })
    })


    function openView(view: DocumentView) {
        router.push({ path: '/document', query: { view: view.id } })
    }


    function deleteView(id: string, event: Event) {
        event.stopPropagation()
        removeView(id)
    }


    function formatDate(ts: number): string {
        const now  = Date.now()
        const diff = now - ts

        const MIN  = 60 * 1000
        const HOUR = 60 * MIN
        const DAY  = 24 * HOUR

        if (diff < MIN)      return 'just now'
        if (diff < HOUR)     return `${Math.floor(diff / MIN)}m ago`
        if (diff < DAY)      return `${Math.floor(diff / HOUR)}h ago`
        if (diff < 7 * DAY)  return `${Math.floor(diff / DAY)}d ago`

        return new Date(ts).toLocaleDateString()
    }


    function axisLabel(view: DocumentView): string {
        const parts: string[] = []
        if (view.xColumn) parts.push(`X: ${view.xColumn}`)
        if (view.yColumn) parts.push(`Y: ${view.yColumn}`)
        if (view.aColumn) parts.push(`A: ${view.aColumn}`)
        return parts.join('  ·  ')
    }
</script>


<template>
    <div class="flex-1 flex flex-col min-h-0 min-w-0 overflow-hidden bg-xrb-bg-1 text-xrb-text-1">
        <div class="flex items-center justify-between px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 shrink-0">
            <h2 class="text-sm tracking-widest">Home</h2>
        </div>

        <div v-if="recentViews.length === 0" class="flex-1 flex items-center justify-center p-6">
            <div class="text-center max-w-md">
                <p class="text-xrb-text-secondary text-sm">
                    No saved views yet.
                </p>
                <p class="text-xrb-text-secondary text-xs mt-2">
                    Open a document, configure it, and click "Save As New" to save a view here.
                </p>
            </div>
        </div>

        <div v-else class="flex-1 overflow-y-auto p-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                <button
                    v-for="view in recentViews"
                    :key="view.id"
                    type="button"
                    class="group relative flex flex-col gap-2 p-4 bg-xrb-bg-2 border border-xrb-border rounded-lg hover:bg-xrb-bg-3 hover:border-xrb-text-secondary transition-colors text-left"
                    @click="openView(view)"
                >
                    <div class="flex items-start justify-between gap-2">
                        <span class="text-sm font-mono text-xrb-text-1 truncate flex-1">
                            {{ view.name || '(unnamed)' }}
                        </span>
                        <button
                            type="button"
                            class="opacity-0 group-hover:opacity-100 btn btn-ghost btn-xs text-xrb-error px-1 transition-opacity"
                            title="Delete view"
                            @click="deleteView(view.id, $event)"
                        >
                            &times;
                        </button>
                    </div>

                    <div v-if="view.table?.source?.name" class="text-xs text-xrb-text-secondary font-mono truncate">
                        {{ view.table.source.name }}
                    </div>

                    <div class="text-xs text-xrb-text-secondary font-mono truncate">
                        {{ axisLabel(view) || '—' }}
                    </div>

                    <div class="flex items-center justify-between text-xs text-xrb-text-secondary font-mono mt-auto pt-1">
                        <span>{{ view.table?.rows?.length ?? 0 }} rows</span>
                        <span>{{ formatDate(view.lastAccessedAt ?? view.savedAt) }}</span>
                    </div>
                </button>
            </div>
        </div>
    </div>
</template>


<style scoped>
</style>
