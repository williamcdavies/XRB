<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';
    import { useApi } from '@/composables/api';
    import {
        type GroupSummary,
        type Member,
        type GroupDetail,
        type FilePermission,
        fetchGroups as fetchGroupsApi,
        fetchGroupDetail,
        createGroupRequest,
        addMemberRequest,
        removeMemberRequest,
        updateRoleRequest,
        deleteGroupRequest,
        fetchFilePermissions,
        setFilePermission,
        deleteFilePermission,
    } from './helpers';

    const { api } = useApi();

    const groups = ref<GroupSummary[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const selectedGroup = ref<GroupDetail | null>(null);
    const loadingDetail = ref(false);

    const showCreateModal = ref(false);
    const newGroupName = ref('');
    const createError = ref<string | null>(null);

    const addEmail = ref('');
    const addError = ref<string | null>(null);
    const isEmailValid = computed(() => !!addEmail.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/));

    const isAdmin = computed(() => selectedGroup.value?.current_user_role === 'admin');

    // File permissions state
    const activeTab = ref<'members' | 'permissions'>('members');
    const filePermissions = ref<FilePermission[]>([]);
    const loadingPermissions = ref(false);
    const showPermissionModal = ref(false);
    const permPath = ref('');
    const permSelectedUserIds = ref<number[]>([]);
    const permError = ref<string | null>(null);
    const editingPermission = ref<FilePermission | null>(null);

    const openMenuMemberId = ref<number | null>(null);

    function toggleMenu(memberId: number) {
        openMenuMemberId.value = openMenuMemberId.value === memberId ? null : memberId;
    }

    function closeMenu() {
        openMenuMemberId.value = null;
    }

    async function fetchGroups() {
        loading.value = true;
        error.value = null;
        try {
            groups.value = await fetchGroupsApi(api);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load groups';
        } finally {
            loading.value = false;
        }
    }

    async function selectGroup(group: { id: number }) {
        loadingDetail.value = true;
        error.value = null;
        activeTab.value = 'members';
        try {
            selectedGroup.value = await fetchGroupDetail(api, group.id);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load group';
        } finally {
            loadingDetail.value = false;
        }
    }

    async function createGroup() {
        const name = newGroupName.value.trim();
        if (!name) return;
        createError.value = null;
        try {
            const data = await createGroupRequest(api, name);
            showCreateModal.value = false;
            newGroupName.value = '';
            await fetchGroups();
            await selectGroup(data);
        } catch (e) {
            createError.value = e instanceof Error ? e.message : 'Failed to create group';
        }
    }

    async function addMember() {
        if (!selectedGroup.value) return;
        const email = addEmail.value.trim();
        if (!email) return;
        addError.value = null;
        try {
            await addMemberRequest(api, selectedGroup.value.id, email);
            addEmail.value = '';
            await selectGroup(selectedGroup.value);
            await fetchGroups();
        } catch (e) {
            addError.value = e instanceof Error ? e.message : 'Failed to add member';
        }
    }

    async function removeMember(member: Member) {
        if (!selectedGroup.value) return;
        if (!confirm(`Remove ${member.email} from ${selectedGroup.value.name}?`)) return;
        try {
            await removeMemberRequest(api, selectedGroup.value.id, member.id);
            await selectGroup(selectedGroup.value);
            await fetchGroups();
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to remove member';
        }
    }

    async function toggleRole(member: Member) {
        if (!selectedGroup.value) return;
        const newRole = member.role === 'admin' ? 'user' : 'admin';
        const action = newRole === 'admin' ? 'Promote' : 'Demote';
        if (!confirm(`${action} ${member.email} to ${newRole}?`)) return;
        try {
            await updateRoleRequest(api, selectedGroup.value.id, member.id, newRole);
            await selectGroup(selectedGroup.value);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to update role';
        }
    }

    async function deleteGroup() {
        if (!selectedGroup.value) return;
        if (!confirm(`Delete group "${selectedGroup.value.name}"? This cannot be undone.`)) return;
        try {
            await deleteGroupRequest(api, selectedGroup.value.id);
            selectedGroup.value = null;
            await fetchGroups();
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to delete group';
        }
    }

    async function loadFilePermissions() {
        if (!selectedGroup.value) return;
        loadingPermissions.value = true;
        try {
            filePermissions.value = await fetchFilePermissions(api, selectedGroup.value.id);
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to load file permissions';
        } finally {
            loadingPermissions.value = false;
        }
    }

    function openPermissionModal(existing?: FilePermission) {
        permError.value = null;
        if (existing) {
            editingPermission.value = existing;
            permPath.value = existing.path;
            permSelectedUserIds.value = existing.allowed_users.map(u => u.id);
        } else {
            editingPermission.value = null;
            permPath.value = '';
            permSelectedUserIds.value = [];
        }
        showPermissionModal.value = true;
    }

    function togglePermUser(userId: number) {
        const idx = permSelectedUserIds.value.indexOf(userId);
        if (idx === -1) {
            permSelectedUserIds.value.push(userId);
        } else {
            permSelectedUserIds.value.splice(idx, 1);
        }
    }

    async function savePermission() {
        if (!selectedGroup.value) return;
        const path = permPath.value.trim();
        if (!path) return;
        permError.value = null;
        try {
            await setFilePermission(api, selectedGroup.value.id, path, permSelectedUserIds.value);
            showPermissionModal.value = false;
            await loadFilePermissions();
        } catch (e) {
            permError.value = e instanceof Error ? e.message : 'Failed to save permission';
        }
    }

    async function removePermission(perm: FilePermission) {
        if (!selectedGroup.value) return;
        if (!confirm(`Remove access restriction on "${perm.path}"? All group members will be able to see it.`)) return;
        try {
            await deleteFilePermission(api, selectedGroup.value.id, perm.path);
            await loadFilePermissions();
        } catch (e) {
            error.value = e instanceof Error ? e.message : 'Failed to remove permission';
        }
    }

    function openCreateModal() {
        newGroupName.value = '';
        createError.value = null;
        showCreateModal.value = true;
    }

    onMounted(fetchGroups);
</script>


<template>
    <div class="flex-1 flex min-h-0 min-w-0 overflow-hidden bg-xrb-bg-1 text-xrb-text-1" @click="closeMenu">
        <!-- Left: group list -->
        <div class="w-1/3 min-w-[240px] flex flex-col border-r border-xrb-border min-h-0">
            <div class="flex items-center justify-between px-4 py-3 border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                <h2 class="text-sm font-medium">Groups</h2>
                <button
                    type="button"
                    class="btn btn-sm btn-outline border-xrb-border text-xrb-text-1 hover:bg-xrb-bg-3"
                    @click="openCreateModal"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                    </svg>
                    New
                </button>
            </div>

            <div v-if="loading" class="flex-1 flex items-center justify-center">
                <span class="loading loading-spinner loading-md"></span>
            </div>

            <div v-else-if="groups.length === 0" class="flex-1 flex items-center justify-center p-4 text-center">
                <p class="text-xrb-text-secondary text-sm">No groups yet. Create one to get started.</p>
            </div>

            <ul v-else class="flex-1 overflow-y-auto">
                <li
                    v-for="group in groups"
                    :key="group.id"
                    class="border-b border-xrb-border"
                >
                    <button
                        type="button"
                        class="w-full px-4 py-3 text-left hover:bg-xrb-bg-3 transition-colors flex items-center justify-between"
                        :class="selectedGroup?.id === group.id ? 'bg-xrb-bg-3' : ''"
                        @click="selectGroup(group)"
                    >
                        <span class="text-sm">{{ group.name }}</span>
                        <span class="text-xs text-xrb-text-secondary">{{ group.member_count }} member{{ group.member_count !== 1 ? 's' : '' }}</span>
                    </button>
                </li>
            </ul>
        </div>

        <!-- Right: group detail -->
        <div class="flex-1 flex flex-col min-h-0 min-w-0">
            <div v-if="!selectedGroup" class="flex-1 flex items-center justify-center">
                <p class="text-xrb-text-secondary text-sm">Select a group to view details</p>
            </div>

            <div v-else-if="loadingDetail" class="flex-1 flex items-center justify-center">
                <span class="loading loading-spinner loading-md"></span>
            </div>

            <template v-else>
                <div class="flex items-center justify-between px-6 py-4 border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                    <h2 class="text-lg font-medium">{{ selectedGroup.name }}</h2>
                    <button
                        v-if="isAdmin"
                        type="button"
                        class="btn btn-sm btn-outline border-red-500/30 text-red-400 hover:bg-red-500/10 hover:border-red-500/50"
                        @click="deleteGroup"
                    >
                        Delete group
                    </button>
                </div>

                <!-- Tabs (admin sees both; regular users only see members) -->
                <div v-if="isAdmin" class="flex border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                    <button
                        type="button"
                        class="px-4 py-2 text-sm transition-colors"
                        :class="activeTab === 'members' ? 'border-b-2 border-xrb-accent-1 text-xrb-text-1' : 'text-xrb-text-secondary hover:text-xrb-text-1'"
                        @click="activeTab = 'members'"
                    >
                        Members
                    </button>
                    <button
                        type="button"
                        class="px-4 py-2 text-sm transition-colors"
                        :class="activeTab === 'permissions' ? 'border-b-2 border-xrb-accent-1 text-xrb-text-1' : 'text-xrb-text-secondary hover:text-xrb-text-1'"
                        @click="activeTab = 'permissions'; loadFilePermissions()"
                    >
                        File Permissions
                    </button>
                </div>

                <!-- MEMBERS TAB -->
                <template v-if="activeTab === 'members'">
                    <!-- Add member (admin only) -->
                    <div v-if="isAdmin" class="px-6 py-3 border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                        <form class="flex items-center gap-2" @submit.prevent="addMember">
                            <input
                                v-model="addEmail"
                                type="email"
                                placeholder="Add member by email"
                                class="input input-sm input-bordered flex-1 bg-xrb-bg-3 border-xrb-border text-xrb-text-1"
                            />
                            <button
                                type="submit"
                                class="btn btn-sm border-xrb-border text-xrb-text-1"
                                :class="isEmailValid ? 'bg-xrb-highlight' : 'bg-xrb-disabled'"
                                :disabled="!isEmailValid"
                            >
                                Add
                            </button>
                        </form>
                        <p v-if="addError" class="mt-1 text-xrb-error text-xs">{{ addError }}</p>
                    </div>

                    <!-- Members list -->
                    <div class="flex-1 overflow-y-auto">
                        <div class="px-6 py-2 text-xs text-xrb-text-secondary uppercase tracking-wider">
                            Members ({{ selectedGroup.members.length }})
                        </div>
                        <ul>
                            <li
                                v-for="member in selectedGroup.members"
                                :key="member.id"
                                class="flex items-center justify-between px-6 py-3 border-b border-xrb-border hover:bg-xrb-bg-3 transition-colors"
                            >
                                <div class="flex items-center gap-2">
                                    <div>
                                        <div class="text-sm">{{ member.email }}</div>
                                        <div v-if="member.first_name || member.last_name" class="text-xs text-xrb-text-secondary">
                                            {{ member.first_name }} {{ member.last_name }}
                                        </div>
                                    </div>
                                    <span
                                        class="text-xs px-1.5 py-0.5 rounded"
                                        :class="member.role === 'admin' ? 'bg-amber-500/20 text-amber-400' : 'bg-xrb-bg-3 text-xrb-text-secondary'"
                                    >
                                        {{ member.role }}
                                    </span>
                                </div>
                                <div v-if="isAdmin" class="relative">
                                    <button
                                        type="button"
                                        class="btn btn-xs btn-ghost text-xrb-text-secondary hover:text-xrb-text-1"
                                        @click.stop="toggleMenu(member.id)"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                                        </svg>
                                    </button>
                                    <div
                                        v-if="openMenuMemberId === member.id"
                                        class="absolute right-0 top-full mt-1 z-20 bg-xrb-bg-2 border border-xrb-border rounded-lg shadow-xl py-1 min-w-[160px]"
                                    >
                                        <button
                                            v-if="member.role === 'user'"
                                            type="button"
                                            class="w-full px-3 py-1.5 text-left text-sm hover:bg-xrb-bg-3 text-amber-400 flex items-center gap-2"
                                            @click="closeMenu(); toggleRole(member)"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
                                            </svg>
                                            Promote to admin
                                        </button>
                                        <button
                                            v-else-if="member.role === 'admin'"
                                            type="button"
                                            class="w-full px-3 py-1.5 text-left text-sm hover:bg-xrb-bg-3 text-blue-400 flex items-center gap-2"
                                            @click="closeMenu(); toggleRole(member)"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                                            </svg>
                                            Demote to user
                                        </button>
                                        <button
                                            type="button"
                                            class="w-full px-3 py-1.5 text-left text-sm hover:bg-xrb-bg-3 text-red-400 flex items-center gap-2"
                                            @click="closeMenu(); removeMember(member)"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                            Remove member
                                        </button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </template>

                <!-- FILE PERMISSIONS TAB (admin only) -->
                <template v-if="activeTab === 'permissions' && isAdmin">
                    <div class="px-6 py-3 border-b border-xrb-border bg-xrb-bg-2 shrink-0">
                        <div class="flex items-center justify-between">
                            <p class="text-xs text-xrb-text-secondary">
                                Restrict files or directories to specific members. Unrestricted paths are visible to all members.
                            </p>
                            <button
                                type="button"
                                class="btn btn-sm btn-outline border-xrb-border text-xrb-text-1 hover:bg-xrb-bg-3"
                                @click="openPermissionModal()"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                </svg>
                                Add restriction
                            </button>
                        </div>
                    </div>

                    <div v-if="loadingPermissions" class="flex-1 flex items-center justify-center">
                        <span class="loading loading-spinner loading-md"></span>
                    </div>

                    <div v-else-if="filePermissions.length === 0" class="flex-1 flex items-center justify-center p-4">
                        <p class="text-xrb-text-secondary text-sm text-center">No file restrictions. All group members can see all files.</p>
                    </div>

                    <div v-else class="flex-1 overflow-y-auto">
                        <ul>
                            <li
                                v-for="perm in filePermissions"
                                :key="perm.id"
                                class="px-6 py-3 border-b border-xrb-border hover:bg-xrb-bg-3 transition-colors"
                            >
                                <div class="flex items-center justify-between">
                                    <div class="min-w-0 flex-1">
                                        <div class="text-sm font-mono truncate">{{ perm.path }}</div>
                                        <div class="text-xs text-xrb-text-secondary mt-1">
                                            <span v-if="perm.allowed_users.length === 0">No users allowed (admins only)</span>
                                            <span v-else>{{ perm.allowed_users.map(u => u.email).join(', ') }}</span>
                                        </div>
                                    </div>
                                    <div class="flex items-center gap-1 shrink-0 ml-2">
                                        <button
                                            type="button"
                                            class="btn btn-xs btn-ghost text-xrb-text-secondary hover:text-xrb-text-1"
                                            title="Edit"
                                            @click="openPermissionModal(perm)"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                            </svg>
                                        </button>
                                        <button
                                            type="button"
                                            class="btn btn-xs btn-ghost text-xrb-text-secondary hover:text-red-400"
                                            title="Remove restriction"
                                            @click="removePermission(perm)"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </template>
            </template>

            <p v-if="error" class="px-6 py-2 text-xrb-error text-sm bg-xrb-bg-2 shrink-0">{{ error }}</p>
        </div>

        <!-- Create group modal -->
        <div v-if="showCreateModal" class="fixed inset-0 z-10 flex items-center justify-center bg-black/50" @click.self="showCreateModal = false">
            <div class="bg-xrb-bg-2 border border-xrb-border rounded-lg p-4 shadow-xl flex flex-col gap-3 min-w-[280px]" @click.stop>
                <h3 class="text-xrb-text-1 font-medium">Create group</h3>
                <input
                    v-model="newGroupName"
                    type="text"
                    class="input input-bordered w-full bg-xrb-bg-3 border-xrb-border text-xrb-text-1"
                    placeholder="Group name"
                    @keydown.enter="createGroup"
                />
                <p v-if="createError" class="text-xrb-error text-sm">{{ createError }}</p>
                <div class="flex justify-end gap-2">
                    <button type="button" class="btn btn-ghost text-xrb-text-secondary" @click="showCreateModal = false">Cancel</button>
                    <button
                        type="button"
                        class="btn bg-xrb-highlight border-xrb-border text-xrb-text-1"
                        :disabled="!newGroupName.trim()"
                        @click="createGroup"
                    >
                        Create
                    </button>
                </div>
            </div>
        </div>

        <!-- File permission modal -->
        <div v-if="showPermissionModal && selectedGroup" class="fixed inset-0 z-10 flex items-center justify-center bg-black/50" @click.self="showPermissionModal = false">
            <div class="bg-xrb-bg-2 border border-xrb-border rounded-lg p-4 shadow-xl flex flex-col gap-3 min-w-[340px] max-w-[440px]" @click.stop>
                <h3 class="text-xrb-text-1 font-medium">
                    {{ editingPermission ? 'Edit' : 'Add' }} file restriction
                </h3>
                <div>
                    <label class="text-xs text-xrb-text-secondary block mb-1">Path (relative to group directory)</label>
                    <input
                        v-model="permPath"
                        type="text"
                        class="input input-bordered w-full bg-xrb-bg-3 border-xrb-border text-xrb-text-1 font-mono text-sm"
                        placeholder="e.g. reports/q1.csv or secret-data"
                        :disabled="!!editingPermission"
                    />
                </div>
                <div>
                    <label class="text-xs text-xrb-text-secondary block mb-1">Allowed members (admins always have access)</label>
                    <div class="max-h-48 overflow-y-auto border border-xrb-border rounded-lg">
                        <label
                            v-for="member in selectedGroup.members.filter(m => m.role !== 'admin')"
                            :key="member.id"
                            class="flex items-center gap-2 px-3 py-2 hover:bg-xrb-bg-3 cursor-pointer transition-colors"
                        >
                            <input
                                type="checkbox"
                                class="checkbox checkbox-sm"
                                :checked="permSelectedUserIds.includes(member.id)"
                                @change="togglePermUser(member.id)"
                            />
                            <span class="text-sm">{{ member.email }}</span>
                        </label>
                        <p v-if="selectedGroup.members.filter(m => m.role !== 'admin').length === 0" class="px-3 py-2 text-xs text-xrb-text-secondary">
                            No non-admin members in this group.
                        </p>
                    </div>
                </div>
                <p v-if="permError" class="text-xrb-error text-sm">{{ permError }}</p>
                <div class="flex justify-end gap-2">
                    <button type="button" class="btn btn-ghost text-xrb-text-secondary" @click="showPermissionModal = false">Cancel</button>
                    <button
                        type="button"
                        class="btn bg-xrb-highlight border-xrb-border text-xrb-text-1"
                        :disabled="!permPath.trim()"
                        @click="savePermission"
                    >
                        Save
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
