<script setup lang="ts">
    import { computed } from 'vue';
    import { formatSize } from './helpers';

    export interface BrowseItem {
        name: string;
        path: string;
        type: 'file' | 'directory';
        size?: number;
        extension?: string;
    }

    const props = defineProps<{
        items: BrowseItem[];
        currentPath: string;
        selectedPath?: string | null;
        loading?: boolean;
        error?: string | null;
        authenticated?: boolean;
    }>();

    const emit = defineEmits<{
        (e: 'open', path: string, type: 'file' | 'directory'): void;
        (e: 'select', path: string): void;
        (e: 'download', path: string): void;
        (e: 'delete', path: string, name: string): void;
    }>();

    function handleClick(item: BrowseItem) {
        if (item.type === 'directory') {
            emit('open', item.path, 'directory');
        } else {
            emit('select', item.path);
        }
    }

    const sortedItems = computed(() => {
        const dirs = props.items.filter((i) => i.type === 'directory').sort((a, b) => a.name.localeCompare(b.name));
        const files = props.items.filter((i) => i.type === 'file').sort((a, b) => a.name.localeCompare(b.name));
        return [...dirs, ...files];
    });

</script>

<template>
    <div class="flex flex-col h-full overflow-hidden bg-xrb-bg-1 text-xrb-text-1">
        <div v-if="error" class="p-4 border-b border-xrb-border bg-xrb-accent-2/20 text-xrb-text-warning-1 rounded m-2">
            {{ error }}
        </div>
        <div v-if="loading" class="flex items-center justify-center flex-1 text-xrb-text-secondary">
            <span class="loading loading-dots loading-lg"></span>
        </div>
        <ul v-else class="menu flex-1 overflow-y-auto p-2 gap-1">
            <li v-for="item in sortedItems" :key="item.path">
                <button type="button"
                    class="flex items-center gap-3 rounded-lg py-2 px-3 border transition-colors text-left w-full group"
                    :class="item.type === 'file' && item.path === selectedPath
                            ? 'bg-xrb-bg-3 border-xrb-border'
                            : 'border-transparent hover:bg-xrb-bg-3 hover:border-xrb-border'
                        " @click="handleClick(item)">
                    <svg v-if="item.type === 'directory'" xmlns="http://www.w3.org/2000/svg" fill="none"
                        viewBox="0 0 24 24" stroke-width="1" stroke="currentColor"
                        class="size-5 shrink-0 text-xrb-accent-1">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                        stroke="currentColor" class="size-5 shrink-0 text-xrb-text-secondary">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                    <span class="flex-1 truncate">{{ item.name }}</span>
                    <span v-if="item.type === 'file' && item.size != null"
                        class="text-xs text-xrb-text-secondary shrink-0">
                        {{ formatSize(item.size) }}
                    </span>
                    <div class="flex items-center gap-1 shrink-0">
                        <button v-if="item.type === 'file'" type="button"
                            class="p-1 rounded hover:bg-xrb-bg-2 text-xrb-text-secondary hover:text-xrb-accent-1 transition-colors"
                            title="Download" @click.stop="emit('download', item.path)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-4">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                        </button>
                        <button v-if="authenticated" type="button"
                            class="p-1 rounded hover:bg-xrb-bg-2 text-xrb-text-secondary hover:text-xrb-error transition-colors"
                            title="Delete" @click.stop="emit('delete', item.path, item.name)">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-4">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                        </button>
                    </div>
                </button>
            </li>
            <li v-if="!loading && !error && sortedItems.length === 0" class="p-4 text-xrb-text-secondary text-sm">
                This folder is empty.
            </li>
        </ul>
    </div>
</template>