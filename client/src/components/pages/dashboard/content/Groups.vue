<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';
    import { useApi } from '@/composables/api';
    import {
        type GroupSummary,
        type Member,
        type GroupDetail,
        fetchGroups as fetchGroupsApi,
        fetchGroupDetail,
        createGroupRequest,
        addMemberRequest,
        removeMemberRequest,
        updateRoleRequest,
        deleteGroupRequest,
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
    </div>
</template>
