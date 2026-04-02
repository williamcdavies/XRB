<script setup lang="ts">
    import { ref, watch, computed } from 'vue';
    import { useApi } from '@/composables/api';

    const LARGE_FILE_THRESHOLD = 100 * 1024 * 1024; // 100 MB

    const props = defineProps<{
        path: string | null;
        fileSize?: number;
    }>();

    const { api } = useApi();

    const loading = ref(false);
    const error = ref<string | null>(null);
    const csvRows = ref<string[][]>([]);
    const csvHeaders = ref<string[]>([]);
    const rawText = ref<string | null>(null);
    const excelSheets = ref<string[]>([]);
    const activeSheet = ref<string>('');
    const needsRowRange = ref(false);
    const rowStart = ref(1);
    const rowEnd = ref(1000);
    const totalRows = ref<number | null>(null);

    const fileName = computed(() => props.path?.split('/').pop() ?? '');

    const TEXT_EXTENSIONS = ['txt', 'json', 'md', 'log', 'py', 'js', 'ts', 'yml', 'yaml', 'toml', 'cfg', 'ini', 'sh'];
    const TABLE_EXTENSIONS = ['csv', 'xlsx', 'xls'];

    function reset() {
        csvRows.value = [];
        csvHeaders.value = [];
        rawText.value = null;
        error.value = null;
        excelSheets.value = [];
        activeSheet.value = '';
        needsRowRange.value = false;
        totalRows.value = null;
    }

    async function loadTable(filePath: string, sheet?: string, startRow?: number, endRow?: number) {
        let url = `/api/data/preview/table/?path=${encodeURIComponent(filePath)}`;
        if (sheet) url += `&sheet=${encodeURIComponent(sheet)}`;
        if (startRow != null) url += `&start_row=${startRow}`;
        if (endRow != null) url += `&end_row=${endRow}`;

        const res = await api.fetch(url);
        if (!res.ok) {
            error.value = `Error ${res.status}`;
            return;
        }
        const data = await res.json();
        csvHeaders.value = data.headers;
        csvRows.value = data.rows;
        excelSheets.value = data.sheets ?? [];
        activeSheet.value = data.active_sheet ?? '';
        if (data.total_rows != null) totalRows.value = data.total_rows;
    }

    async function switchSheet(sheet: string) {
        if (!props.path || sheet === activeSheet.value) return;
        loading.value = true;
        csvHeaders.value = [];
        csvRows.value = [];
        error.value = null;
        try {
            await loadTable(props.path, sheet);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load sheet';
        } finally {
            loading.value = false;
        }
    }

    async function loadRowRange() {
        if (!props.path) return;
        loading.value = true;
        error.value = null;
        needsRowRange.value = false;
        try {
            await loadTable(props.path, undefined, rowStart.value, rowEnd.value);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load preview';
        } finally {
            loading.value = false;
        }
    }

    async function loadPreview(filePath: string) {
        loading.value = true;
        reset();

        const ext = filePath.split('.').pop()?.toLowerCase() ?? '';

        if (!TEXT_EXTENSIONS.includes(ext) && !TABLE_EXTENSIONS.includes(ext)) {
            loading.value = false;
            return;
        }

        try {
            if (TABLE_EXTENSIONS.includes(ext)) {
                if (props.fileSize != null && props.fileSize > LARGE_FILE_THRESHOLD) {
                    needsRowRange.value = true;
                    rowStart.value = 1;
                    rowEnd.value = 1000;
                    loading.value = false;
                    return;
                }
                await loadTable(filePath);
            } else {
                const res = await api.fetch(`/api/data/download/?path=${encodeURIComponent(filePath)}`);
                if (!res.ok) {
                    error.value = `Error ${res.status}`;
                    return;
                }
                rawText.value = await res.text();
            }
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load preview';
        } finally {
            loading.value = false;
        }
    }

    watch(() => props.path, (newPath) => {
        if (newPath) {
            loadPreview(newPath);
        } else {
            reset();
        }
    }, { immediate: true });
</script>

<template>
    <div class="flex flex-col h-full overflow-hidden bg-xrb-bg-1 text-xrb-text-1">
        <!-- No file selected -->
        <div v-if="!path" class="flex-1 flex items-center justify-center text-xrb-text-secondary text-sm">
            Select a file to preview
        </div>

        <!-- Loading -->
        <div v-else-if="loading" class="flex-1 flex items-center justify-center text-xrb-text-secondary">
            <span class="loading loading-dots loading-lg"></span>
        </div>

        <!-- Large file row range prompt -->
        <div v-else-if="needsRowRange" class="flex flex-col flex-1">
            <div class="px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 text-sm font-medium truncate">
                {{ fileName }}
            </div>
            <div class="flex-1 flex flex-col items-center justify-center gap-4 p-6 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                    stroke="currentColor" class="size-10 opacity-40 text-xrb-text-secondary">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
                </svg>
                <p class="text-xrb-text-secondary text-sm">
                    This file is larger than 100 MB. Select a range of rows to preview.
                </p>
                <div class="flex items-center gap-2">
                    <label class="text-xs text-xrb-text-secondary">Rows</label>
                    <input v-model.number="rowStart" type="number" min="1"
                        class="input input-sm input-bordered w-24 bg-xrb-bg-3 border-xrb-border text-xrb-text-1" />
                    <span class="text-xrb-text-secondary">to</span>
                    <input v-model.number="rowEnd" type="number" :min="rowStart"
                        class="input input-sm input-bordered w-24 bg-xrb-bg-3 border-xrb-border text-xrb-text-1" />
                </div>
                <button type="button"
                    class="btn btn-sm bg-xrb-highlight border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:text-xrb-text-2"
                    :disabled="rowStart < 1 || rowEnd < rowStart"
                    @click="loadRowRange">
                    Load preview
                </button>
            </div>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="flex flex-col flex-1">
            <div class="px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 text-sm font-medium truncate">
                {{ fileName }}
            </div>
            <div class="p-4 text-xrb-error text-sm">{{ error }}</div>
        </div>

        <!-- CSV / Excel table preview -->
        <div v-else-if="csvHeaders.length > 0" class="flex flex-col flex-1 min-h-0">
            <div
                class="px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 text-sm font-medium truncate flex items-center gap-2">
                <span class="truncate">{{ fileName }}</span>
                <span class="text-xs text-xrb-text-secondary shrink-0">
                    {{ csvRows.length }} rows{{ totalRows != null ? ` (of ${totalRows} total)` : '' }}
                </span>
            </div>
            <!-- Sheet tabs for Excel files -->
            <div v-if="excelSheets.length > 1"
                class="flex gap-0 border-b border-xrb-border bg-xrb-bg-2 px-2 overflow-x-auto">
                <button v-for="sheet in excelSheets" :key="sheet" @click="switchSheet(sheet)" :class="[
                    'px-3 py-1.5 text-xs border-b-2 whitespace-nowrap transition-colors',
                    sheet === activeSheet
                        ? 'border-xrb-accent text-xrb-accent font-medium'
                        : 'border-transparent text-xrb-text-secondary hover:text-xrb-text-1',
                ]">
                    {{ sheet }}
                </button>
            </div>
            <div class="flex-1 overflow-auto">
                <table class="table table-xs table-pin-rows w-full">
                    <thead>
                        <tr class="bg-xrb-bg-2">
                            <th v-for="header in csvHeaders" :key="header"
                                class="text-xrb-text-secondary font-medium text-xs px-3 py-2 border-b border-xrb-border">
                                {{ header }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(row, i) in csvRows" :key="i" class="hover:bg-xrb-bg-2">
                            <td v-for="(cell, j) in row" :key="j"
                                class="px-3 py-1.5 text-xs border-b border-xrb-border/50 whitespace-nowrap">
                                {{ cell }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Raw text preview -->
        <div v-else-if="rawText != null" class="flex flex-col flex-1 min-h-0">
            <div class="px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 text-sm font-medium truncate">
                {{ fileName }}
            </div>
            <pre
                class="flex-1 overflow-auto p-4 text-xs leading-relaxed whitespace-pre-wrap break-words font-mono text-xrb-text-secondary">{{ rawText }}</pre>
        </div>

        <!-- Not previewable -->
        <div v-else class="flex flex-col flex-1">
            <div class="px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 text-sm font-medium truncate">
                {{ fileName }}
            </div>
            <div class="flex-1 flex flex-col items-center justify-center gap-2 text-xrb-text-secondary text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                    stroke="currentColor" class="size-10 opacity-40">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                <span>No preview available for this file type</span>
            </div>
        </div>
    </div>
</template>
