<script setup lang="ts">
    import { ref, computed, watch, onMounted } from 'vue';
    import { useApi } from '@/composables/api';
    import FileList from './FileList.vue';
    import FilePreview from './FilePreview.vue';
    import type { BrowseItem } from './FileList.vue';
    import {
        browsePath,
        downloadFile,
        deleteItem,
        uploadFile,
        createDirectory,
    } from './helpers';
import { useAuth } from '@/composables/auth';

    const { api } = useApi();
    const { isAuthenticated } = useAuth()
    const authenticated = ref(false)

    type TabId = 'public' | 'user';

    const activeTab = ref<TabId>('public');
    const username = ref<string | null>(null);

    const currentPath = ref('');
    const items = ref<BrowseItem[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const dirExists = ref(true);
    const uploading = ref(false);
    const uploadError = ref<string | null>(null);
    const uploadInput = ref<HTMLInputElement | null>(null);
    const creatingDir = ref(false);
    const newDirName = ref('');
    const createDirError = ref<string | null>(null);

    const selectedFile = ref<string | null>(null);

    const tabs = computed(() => {
        const t: { id: TabId; label: string; rootPath: string }[] = [
            { id: 'public', label: 'Public', rootPath: 'public' },
        ];
        if (username.value) {
            t.push({ id: 'user', label: 'User', rootPath: `users/${username.value}` });
        }
        return t;
    });

    const currentRootPath = computed(() => {
        const t = tabs.value.find((x) => x.id === activeTab.value);
        return t ? t.rootPath : 'public';
    });

    const displayItems = computed(() => items.value);

    function loadParent() {
        const parts = currentPath.value.split('/');
        parts.pop();
        const parent = parts.join('/') || currentRootPath.value;
        selectedFile.value = null;
        loadPath(parent);
    }

    async function loadPath(path: string, extractUsername = false) {
        loading.value = true;
        error.value = null;
        try {
            const result = await browsePath(api, path, extractUsername);
            items.value = result.items;
            currentPath.value = result.path;
            if (extractUsername) {
                username.value = result.username;
            }
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load';
            items.value = [];
        } finally {
            loading.value = false;
        }
    }

    async function goToTabRoot() {
        selectedFile.value = null;
        currentPath.value = currentRootPath.value;
        if (activeTab.value === 'user' && username.value) {
            loading.value = true;
            error.value = null;
            try {
                const check = await browsePath(api, 'users');
                dirExists.value = check.items.some((i) => i.path === `users/${username.value}`);
                if (dirExists.value) {
                    const result = await browsePath(api, currentRootPath.value);
                    items.value = result.items;
                    currentPath.value = result.path;
                } else {
                    items.value = [];
                }
            } catch (e) {
                error.value = e instanceof Error ? e.message : 'Failed to load';
                items.value = [];
            } finally {
                loading.value = false;
            }
        } else {
            dirExists.value = true;
            loadPath(currentRootPath.value);
        }
    }

    async function initPersonalDir() {
        if (!username.value) return;
        error.value = null;
        try {
            await createDirectory(api, 'users', username.value);
            await goToTabRoot();
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to create personal directory';
        }
    }

    watch(activeTab, () => {
        goToTabRoot();
    });

    function onOpen(path: string, type: 'file' | 'directory') {
        if (type === 'directory') {
            loadPath(path);
        }
    }

    async function handleDownload(relativePath: string) {
        try {
            await downloadFile(api, relativePath);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Download failed';
        }
    }

    async function handleDelete(path: string, name: string) {
        if (!confirm(`Delete "${name}"?`)) return;
        try {
            await deleteItem(api, path);
            if (selectedFile.value === path) {
                selectedFile.value = null;
            }
            await loadPath(currentPath.value || currentRootPath.value);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Delete failed';
        }
    }

    async function onFileSelected(ev: Event) {
        const input = ev.target as HTMLInputElement;
        const file = input.files?.[0];
        input.value = '';
        if (!file) return;
        uploading.value = true;
        uploadError.value = null;
        try {
            await uploadFile(api, file, currentPath.value || currentRootPath.value);
            await loadPath(currentPath.value || currentRootPath.value);
        } catch (e) {
            uploadError.value = e instanceof Error ? e.message : 'Upload failed';
        } finally {
            uploading.value = false;
        }
    }

    const uploadTargetPath = computed(() => currentPath.value || currentRootPath.value);

    function openNewDirForm() {
        newDirName.value = '';
        createDirError.value = null;
        creatingDir.value = true;
    }

    function cancelNewDir() {
        creatingDir.value = false;
        newDirName.value = '';
        createDirError.value = null;
    }

    async function submitNewDir() {
        const name = newDirName.value.trim();
        if (!name) return;
        createDirError.value = null;
        try {
            await createDirectory(api, uploadTargetPath.value, name);
            cancelNewDir();
            await loadPath(currentPath.value || currentRootPath.value);
        } catch (e) {
            createDirError.value = e instanceof Error ? e.message : 'Failed to create directory';
        }
    }

    onMounted(async () => {
        authenticated.value = await isAuthenticated();
        loadPath('', true).then(() => {
            currentPath.value = currentRootPath.value;
            loadPath(currentRootPath.value);
        });
    });
</script>

<template>
    <div class="flex-1 flex flex-col min-h-0 min-w-0 overflow-hidden bg-xrb-bg-1 text-xrb-text-1">
        <!-- Top bar: tabs -->
        <div class="flex items-center border-b border-xrb-border bg-xrb-bg-2 shrink-0">
            <button v-for="tab in tabs" :key="tab.id" type="button"
                class="px-6 py-3 text-sm font-medium border-b-2 transition-colors" :class="activeTab === tab.id
                        ? 'border-xrb-accent-1 text-xrb-accent-1'
                        : 'border-transparent text-xrb-text-secondary hover:text-xrb-text-1'
                    " @click="activeTab = tab.id">
                {{ tab.label }}
            </button>
        </div>

        <!-- Split: left = file browser, right = preview -->
        <div class="flex-1 flex min-h-0 overflow-hidden">
            <!-- Left panel -->
            <div class="w-1/3 min-w-0 flex flex-col border-r border-xrb-border min-h-0">
                <!-- Personal directory missing prompt -->
                <div
                    v-if="!dirExists && activeTab === 'user'"
                    class="flex-1 flex flex-col items-center justify-center gap-3 p-6 text-center"
                >
                    <p class="text-xrb-text-secondary text-sm">Your personal directory does not exist yet.</p>
                    <button
                        type="button"
                        class="btn btn-sm bg-xrb-highlight border-xrb-border text-xrb-text-1"
                        @click="initPersonalDir"
                    >
                        Create personal directory
                    </button>
                    <p v-if="error" class="text-xrb-error text-sm">{{ error }}</p>
                </div>

                <template v-else>
                <!-- Parent directory button -->
                <button v-if="currentPath && currentPath !== currentRootPath" type="button"
                    class="flex items-center gap-2 px-4 py-2 text-sm text-xrb-text-secondary hover:text-xrb-accent-1 hover:bg-xrb-bg-3 border-b border-xrb-border transition-colors shrink-0"
                    @click="loadParent">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-4">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                    </svg>
                    ..
                </button>
                <div class="flex-1 min-h-0">
                    <FileList :items="displayItems" :current-path="currentPath" :selected-path="selectedFile"
                        :loading="loading" :error="error" :authenticated="authenticated" @open="onOpen" @select="(path) => selectedFile = path"
                        @download="handleDownload" @delete="handleDelete" />
                </div>

                <!-- Actions bar -->
                <div v-if="authenticated" class="p-3 border-t border-xrb-border bg-xrb-bg-2 flex flex-wrap items-center gap-3 shrink-0">
                    <button type="button"
                        class="btn btn-sm btn-outline border-xrb-border text-xrb-text-1 hover:bg-xrb-bg-3 hover:border-xrb-border"
                        @click="openNewDirForm">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                            stroke="currentColor" class="size-4">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>
                        New directory
                    </button>
                    <input ref="uploadInput" type="file" class="hidden" @change="onFileSelected" />
                    <button type="button"
                        class="btn btn-sm btn-outline bg-xrb-highlight border-xrb-border text-xrb-text-1 hover:bg-xrb-text-1 hover:border-xrb-text-1 hover:text-xrb-text-2 disabled:opacity-50"
                        :disabled="uploading" @click="uploadInput?.click">
                        <span v-if="uploading" class="loading loading-spinner loading-sm"></span>
                        <span v-else>Upload file</span>
                    </button>
                    <span v-if="uploadTargetPath" class="text-xs text-xrb-text-secondary break-all">
                        into {{ uploadTargetPath }}
                    </span>
                </div>
                <div v-if="uploadError" class="px-3 pb-2 text-xrb-error text-sm bg-xrb-bg-2 shrink-0">
                    {{ uploadError }}
                </div>
                </template>
            </div>

            <!-- Right panel: preview -->
            <div class="w-2/3 min-w-0 min-h-0 overflow-hidden">
                <FilePreview :path="selectedFile" />
            </div>
        </div>

        <!-- New directory modal -->
        <div v-if="creatingDir" class="fixed inset-0 z-10 flex items-center justify-center bg-black/50"
            @click.self="cancelNewDir">
            <div class="bg-xrb-bg-2 border border-xrb-border rounded-lg p-4 shadow-xl flex flex-col gap-3 min-w-[280px]"
                @click.stop>
                <h3 class="text-xrb-text-1 font-medium">New directory</h3>
                <input v-model="newDirName" type="text"
                    class="input input-bordered w-full bg-xrb-bg-3 border-xrb-border text-xrb-text-1"
                    placeholder="Directory name" @keydown.enter="submitNewDir" />
                <p v-if="createDirError" class="text-xrb-error text-sm">{{ createDirError }}</p>
                <div class="flex justify-end gap-2">
                    <button type="button" class="btn btn-ghost text-xrb-text-secondary"
                        @click="cancelNewDir">Cancel</button>
                    <button type="button" class="btn bg-xrb-highlight border-xrb-border text-xrb-text-1"
                        :disabled="!newDirName.trim()" @click="submitNewDir">
                        Create
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>