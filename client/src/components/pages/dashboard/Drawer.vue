<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useAuth } from '@/composables/auth';
import { useUser } from '@/composables/account'
import { computed } from 'vue'
import { useDocumentViews } from '@/composables/views'
import type { DocumentView } from '@/types/view'

const activeView = ref('home')

// Ref: https://vuejs.org/guide/components/events.html
const emit = defineEmits<{
    changeView: [view: string]
}>();

const router = useRouter();
const { views } = useDocumentViews();

const recentViews = computed(() => {
    return [...views.value].sort((a, b) => {
        const aTime = a.lastAccessedAt ?? a.savedAt
        const bTime = b.lastAccessedAt ?? b.savedAt
        return bTime - aTime
    }).slice(0, 5)
})

function truncateName(name: string) {
    return name.length > 20 ? name.slice(0, 20) + '...' : name
}

function openView(view: DocumentView) {
    router.push({ path: '/document', query: { view: view.id } })
}

const { isAuthenticated } = useAuth()
const authenticated = ref(false)

const { user, fetchUser } = useUser()

onMounted(async () => {
    authenticated.value = await isAuthenticated()
    if (authenticated.value) {
        await fetchUser()
    } else {
        console.log('No valid token found')
    }
})


const handleNavigation = (view: string) => {
    if (view === 'document') {
        router.push('/document');
    } else {
        activeView.value = view;
        emit('changeView', view);
    }
};

const isActive = (view: string) => activeView.value === view
</script>


<template>
    <!-- ref: https://daisyui.com/components/drawer/?lang=en, https://heroicons.com -->
    <div class="drawer drawer-open">
        <input id="dashboard-drawer" type="checkbox" class="drawer-toggle" />
        <div class="drawer-side is-drawer-close:overflow-visible">
            <div
                class="flex min-h-full flex-col items-start bg-xrb-drawer-background is-drawer-close:w-14 is-drawer-open:w-64 border-r border-xrb-border-1 transition-[width] duration-300">
                <!-- Sidebar content here -->
                <ul class="menu w-full grow p-0 gap-1">
                    <!-- Sidebar -->
                    <li class="pb-8">
                        <label for="dashboard-drawer" aria-label="toggle sidebar"
                            class="p-4 is-drawer-open:ml-auto cursor-pointer rounded-none tooltip tooltip-right tooltip-neutral group"
                            data-tip="Toggle Sidebar">
                            <!-- Sidebar toggle icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-linejoin="round"
                                stroke-linecap="round" stroke-width="1" stroke="currentColor" fill="none"
                                class="inline-block size-6 transition-colors duration-50">
                                <path
                                    d="M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z" />
                                <path d="M9 4v16" />
                            </svg>
                        </label>
                    </li>

                    <!-- New item -->
                    <li>
                        <button @click="handleNavigation('document')"
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group text-xrb-text-secondary hover:text-xrb-text-primary"
                            data-tip="New">
                            <!-- New item icon -->
                            <svg v-if="isActive('new')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                fill="currentColor" class="size-6">
                                <path fill-rule="evenodd"
                                    d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 9a.75.75 0 0 0-1.5 0v2.25H9a.75.75 0 0 0 0 1.5h2.25V15a.75.75 0 0 0 1.5 0v-2.25H15a.75.75 0 0 0 0-1.5h-2.25V9Z"
                                    clip-rule="evenodd" />
                            </svg>

                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1" stroke="currentColor" class="size-6 transition-colors duration-50">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span class="is-drawer-close:hidden select-none leading-6">New</span>
                        </button>
                    </li>

                    <!-- Home item -->
                    <li>
                        <button @click="handleNavigation('home')"
                            :class="isActive('home') ? 'text-xrb-text-primary' : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Home">
                            <!-- Home icon -->
                            <svg v-if="isActive('home')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                fill="currentColor" class="size-6">
                                <path
                                    d="M11.47 3.841a.75.75 0 0 1 1.06 0l8.69 8.69a.75.75 0 1 0 1.06-1.061l-8.689-8.69a2.25 2.25 0 0 0-3.182 0l-8.69 8.69a.75.75 0 1 0 1.061 1.06l8.69-8.689Z" />
                                <path
                                    d="m12 5.432 8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 0 1-.75-.75v-4.5a.75.75 0 0 0-.75-.75h-3a.75.75 0 0 0-.75.75V21a.75.75 0 0 1-.75.75H5.625a1.875 1.875 0 0 1-1.875-1.875v-6.198a2.29 2.29 0 0 0 .091-.086L12 5.432Z" />
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1" stroke="currentColor" class="size-6 transition-colors duration-50">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                            </svg>
                            <span class="is-drawer-close:hidden select-none leading-6">Home</span>
                        </button>
                    </li>

                    <!-- Files item -->
                    <li>
                        <button @click="handleNavigation('files')"
                            :class="isActive('files') ? 'text-xrb-text-primary' : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Files">
                            <svg v-if="isActive('files')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                fill="currentColor" class="size-6">
                                <path
                                    d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0 0 16.5 9h-1.875a1.875 1.875 0 0 1-1.875-1.875V5.25A3.75 3.75 0 0 0 9 1.5H5.625Z" />
                                <path
                                    d="M12.971 1.816A5.23 5.23 0 0 1 14.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 0 1 3.434 1.279 9.768 9.768 0 0 0-6.963-6.963Z" />
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1" stroke="currentColor" class="size-6 transition-colors duration-50">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                            </svg>


                            <span class="is-drawer-close:hidden select-none leading-6">Files</span>
                        </button>
                    </li>

                    <!-- Groups item -->
                    <li v-if="authenticated">
                        <button @click="handleNavigation('groups')"
                            :class="isActive('groups') ? 'text-xrb-text-primary' : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Groups">
                            <!-- Groups icon -->
                            <svg v-if="isActive('groups')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                fill="currentColor" class="size-6">
                                <path
                                    d="M19.5 21a3 3 0 0 0 3-3v-4.5a3 3 0 0 0-3-3h-15a3 3 0 0 0-3 3V18a3 3 0 0 0 3 3h15ZM1.5 10.146V6a3 3 0 0 1 3-3h5.379a2.25 2.25 0 0 1 1.59.659l2.122 2.121c.14.141.331.22.53.22H19.5a3 3 0 0 1 3 3v1.146A4.483 4.483 0 0 0 19.5 9h-15a4.483 4.483 0 0 0-3 1.146Z" />
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1" stroke="currentColor" class="size-6 transition-colors duration-50">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5
                                    1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75
                                    18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                            </svg>
                            <span class="is-drawer-close:hidden select-none leading-6">Groups</span>
                        </button>
                    </li>

                    <!-- Learn item -->
                    <li v-if="authenticated && user?.type === 'Student'">
                        <button @click="handleNavigation('learn')"
                            :class="isActive('learn') ? 'text-xrb-text-primary' : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Learn">
                            <!-- Learn icon -->
                            <svg v-if="isActive('learn')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                fill="currentColor" class="size-6">
                                <path
                                    d="M11.7 2.805a.75.75 0 0 1 .6 0A60.65 60.65 0 0 1 22.83 8.72a.75.75 0 0 1-.231 1.337 49.948 49.948 0 0 0-9.902 3.912l-.003.002c-.114.06-.227.119-.34.18a.75.75 0 0 1-.707 0A50.88 50.88 0 0 0 7.5 12.173v-.224c0-.131.067-.248.172-.311a54.615 54.615 0 0 1 4.653-2.52.75.75 0 0 0-.65-1.352 56.123 56.123 0 0 0-4.78 2.589 1.858 1.858 0 0 0-.859 1.228 49.803 49.803 0 0 0-4.634-1.527.75.75 0 0 1-.231-1.337A60.653 60.653 0 0 1 11.7 2.805Z" />
                                <path
                                    d="M13.06 15.473a48.45 48.45 0 0 1 7.666-3.282c.134 1.414.22 2.843.255 4.284a.75.75 0 0 1-.46.711 47.87 47.87 0 0 0-8.105 4.342.75.75 0 0 1-.832 0 47.87 47.87 0 0 0-8.104-4.342.75.75 0 0 1-.461-.71c.035-1.442.121-2.87.255-4.286.921.304 1.83.634 2.726.99v1.27a1.5 1.5 0 0 0-.14 2.508c-.09.38-.222.753-.397 1.11.452.213.901.434 1.346.66a6.727 6.727 0 0 0 .551-1.607 1.5 1.5 0 0 0 .14-2.67v-.645a48.549 48.549 0 0 1 3.44 1.667 2.25 2.25 0 0 0 2.12 0Z" />
                                <path
                                    d="M4.462 19.462c.42-.419.753-.89 1-1.395.453.214.902.435 1.347.662a6.742 6.742 0 0 1-1.286 1.794.75.75 0 0 1-1.06-1.06Z" />
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1" stroke="currentColor" class="size-6 transition-colors duration-50">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 
                                48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 
                                0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 
                                0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 
                                0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                            </svg>
                            <span class="is-drawer-close:hidden select-none leading-6">Learn</span>
                        </button>
                    </li>

                    <!-- Recents -->
                    <div>
                        <span
                            class="item-inline is-drawer-close:hidden p-4 text-xrb-text-secondary flex justify-start select-none">Recents</span>
                        <button v-for="view in recentViews" :key="view.id" type="button"
                            class="w-full rounded-none is-drawer-close:hidden group relative flex flex-col pl-6 py-2 text-left cursor-pointer text-xrb-text-secondary hover:text-xrb-text-primary hover:bg-base-content/10 transition-colors duration-50"
                            @click="openView(view)">
                            <div class="flex items-center justify-between select-none">
                                <span class="text-sm truncate flex-1">
                                    {{ truncateName(view.name || '(unnamed)') }}
                                </span>
                            </div>
                        </button>
                    </div>

                    <!-- Force to Bottom -->
                    <div class="mt-auto border-t-1 border-xrb-border-1">
                        <!-- Account item -->
                        <li v-if="authenticated">
                            <button @click="handleNavigation('account')"
                                :class="isActive('account') ? 'text-xrb-text-primary' : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
                                class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Account">
                                <!-- Account icon -->
                                <svg v-if="isActive('account')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                    fill="currentColor" class="size-6">
                                    <path fill-rule="evenodd"
                                        d="M18.685 19.097A9.723 9.723 0 0 0 21.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 0 0 3.065 7.097A9.716 9.716 0 0 0 12 21.75a9.716 9.716 0 0 0 6.685-2.653Zm-12.54-1.285A7.486 7.486 0 0 1 12 15a7.486 7.486 0 0 1 5.855 2.812A8.224 8.224 0 0 1 12 20.25a8.224 8.224 0 0 1-5.855-2.438ZM15.75 9a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z"
                                        clip-rule="evenodd" />
                                </svg>
                                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1" stroke="currentColor" class="size-6 transition-colors duration-50">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 
                                    0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 
                                    9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg>
                                <span class="is-drawer-close:hidden select-none leading-6">Account</span>
                            </button>
                        </li>
                    </div>

                </ul>
            </div>
        </div>
    </div>
</template>


<style scoped></style>