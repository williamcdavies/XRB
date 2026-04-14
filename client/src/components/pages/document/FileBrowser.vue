<script setup lang="ts">
    import { ref, computed, watch, onMounted } from 'vue';
    import { useApi }   from '@/composables/api';
    import { useAuth }  from '@/composables/auth';
    import { browsePath } from '@/components/pages/files/helpers';
    import FileList from '@/components/pages/files/FileList.vue';
    import type { BrowseItem } from '@/components/pages/files/FileList.vue';


    const emit = defineEmits<{
        (e: 'close'): void
        (e: 'select', path: string): void
    }>()


    const { api }             = useApi()
    const { isAuthenticated } = useAuth()


    type TabId = string

    const authenticated = ref(false)
    const username      = ref<string | null>(null)
    const userGroups    = ref<{ name: string; path: string }[]>([])

    const activeTab   = ref<TabId>('public')
    const currentPath = ref('')
    const items       = ref<BrowseItem[]>([])
    const loading     = ref(false)
    const error       = ref<string | null>(null)


    const mainTabs = computed(() => {
        const t: { id: string; label: string }[] = [
            { id: 'public', label: 'Public' },
        ]
        if (username.value) {
            t.push({ id: 'user', label: 'User' })
        }
        if (userGroups.value.length > 0) {
            t.push({ id: 'groups', label: 'Groups' })
        }
        return t
    })


    const activeMainTab = computed(() => {
        if (activeTab.value.startsWith('group:')) return 'groups'
        return activeTab.value
    })


    const activeGroupName = computed(() => {
        if (!activeTab.value.startsWith('group:')) return null
        return activeTab.value.slice('group:'.length)
    })


    const tabs = computed(() => {
        const t: { id: TabId; rootPath: string }[] = [
            { id: 'public', rootPath: 'public' },
        ]
        if (username.value) {
            t.push({ id: 'user', rootPath: `users/${username.value}` })
        }
        for (const g of userGroups.value) {
            t.push({ id: `group:${g.name}`, rootPath: g.path })
        }
        return t
    })


    const currentRootPath = computed(() => {
        const t = tabs.value.find((x) => x.id === activeTab.value)
        return t ? t.rootPath : 'public'
    })


    // only show directories and .csv files
    const visibleItems = computed(() =>
        items.value.filter((i) => i.type === 'directory' || i.extension === '.csv')
    )


    function selectMainTab(id: string) {
        if (id === 'groups') {
            if (!activeTab.value.startsWith('group:') && userGroups.value.length > 0) {
                activeTab.value = `group:${userGroups.value[0]!.name}`
            }
        } else {
            activeTab.value = id
        }
    }


    async function loadPath(path: string) {
        loading.value = true
        error.value   = null
        try {
            const result      = await browsePath(api, path)
            items.value       = result.items
            currentPath.value = result.path
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load'
            items.value = []
        } finally {
            loading.value = false
        }
    }


    function loadParent() {
        const parts = currentPath.value.split('/')
        parts.pop()
        const parent = parts.join('/') || currentRootPath.value
        loadPath(parent)
    }


    function onOpen(path: string, type: 'file' | 'directory') {
        if (type === 'directory') {
            loadPath(path)
        }
    }


    function onSelect(path: string) {
        emit('select', path)
    }


    watch(activeTab, () => {
        loadPath(currentRootPath.value)
    })


    onMounted(async () => {
        authenticated.value = await isAuthenticated()
        try {
            const result = await browsePath(api, '', true)
            username.value   = result.username
            userGroups.value = result.items
                .filter((i) => i.type === 'directory' && i.path.startsWith('groups/'))
                .map((i) => ({ name: i.name, path: i.path }))
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load'
        }
        await loadPath(currentRootPath.value)
    })
</script>


<template>
    <div class="fixed inset-0 z-20 flex items-center justify-center bg-black/50" @click.self="emit('close')">
        <div class="bg-xrb-bg-1 border border-xrb-border rounded-lg shadow-xl flex flex-col w-[640px] h-[520px] max-w-[90vw] max-h-[90vh]"
            @click.stop>
            <!-- Header -->
            <div class="flex items-center justify-between px-4 py-3 border-b border-xrb-border bg-xrb-bg-2">
                <h3 class="text-xrb-text-1 font-mono text-sm uppercase tracking-widest">Select CSV file</h3>
                <button type="button" class="btn btn-ghost btn-xs text-xrb-text-secondary"
                    @click="emit('close')">Close</button>
            </div>

            <!-- Main tabs -->
            <div class="flex items-center border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                <button v-for="tab in mainTabs" :key="tab.id" type="button"
                    class="px-5 py-2 text-xs font-medium border-b-2 transition-colors"
                    :class="activeMainTab === tab.id
                        ? 'border-xrb-accent-1 text-xrb-accent-1'
                        : 'border-transparent text-xrb-text-secondary hover:text-xrb-text-1'"
                    @click="selectMainTab(tab.id)">
                    {{ tab.label }}
                </button>
            </div>

            <!-- Group sub-tabs -->
            <div v-if="activeMainTab === 'groups'"
                class="flex items-center border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                <button v-for="g in userGroups" :key="g.name" type="button"
                    class="px-5 py-1.5 text-xs font-medium border-b-2 transition-colors"
                    :class="activeGroupName === g.name
                        ? 'border-xrb-accent-1 text-xrb-accent-1'
                        : 'border-transparent text-xrb-text-secondary hover:text-xrb-text-1'"
                    @click="activeTab = `group:${g.name}`">
                    {{ g.name }}
                </button>
            </div>

            <!-- Parent button -->
            <button v-if="currentPath && currentPath !== currentRootPath" type="button"
                class="flex items-center gap-2 px-4 py-2 text-xs text-xrb-text-secondary hover:text-xrb-accent-1 hover:bg-xrb-bg-3 border-b border-xrb-border transition-colors shrink-0"
                @click="loadParent">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-4">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                </svg>
                <span class="truncate">{{ currentPath }}</span>
            </button>

            <!-- File list -->
            <div class="flex-1 min-h-0 overflow-hidden">
                <FileList
                    :items="visibleItems"
                    :current-path="currentPath"
                    :loading="loading"
                    :error="error"
                    :show-actions="false"
                    @open="onOpen"
                    @select="onSelect" />
            </div>
        </div>
    </div>
</template>
