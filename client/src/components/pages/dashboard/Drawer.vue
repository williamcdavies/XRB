<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useAuth } from '@/composables/auth';

const { isAuthenticated } = useAuth()
const authenticated = ref(false)

onMounted(async () => {
    authenticated.value = await isAuthenticated()
})

const activeView = ref('home')

// Ref: https://vuejs.org/guide/components/events.html
const emit = defineEmits<{
    changeView: [view: string]
}>();

const router = useRouter();

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
                                class="inline-block size-6 transition-colors duration-300">
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
                            <svg v-if="isActive('new')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                                class="size-6">
                                <path fill-rule="evenodd"
                                    d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 9a.75.75 0 0 0-1.5 0v2.25H9a.75.75 0 0 0 0 1.5h2.25V15a.75.75 0 0 0 1.5 0v-2.25H15a.75.75 0 0 0 0-1.5h-2.25V9Z"
                                    clip-rule="evenodd" />
                            </svg>

                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor" class="size-6 transition-colors duration-50">
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
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group"
                            data-tip="Home">
                            <!-- Home icon -->
                            <svg v-if="isActive('home')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                                fill="currentColor" class="size-6">
                                <path
                                    d="M11.47 3.841a.75.75 0 0 1 1.06 0l8.69 8.69a.75.75 0 1 0 1.06-1.061l-8.689-8.69a2.25 2.25 0 0 0-3.182 0l-8.69 8.69a.75.75 0 1 0 1.061 1.06l8.69-8.689Z" />
                                <path
                                    d="m12 5.432 8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 0 1-.75-.75v-4.5a.75.75 0 0 0-.75-.75h-3a.75.75 0 0 0-.75.75V21a.75.75 0 0 1-.75.75H5.625a1.875 1.875 0 0 1-1.875-1.875v-6.198a2.29 2.29 0 0 0 .091-.086L12 5.432Z" />
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-6 transition-colors duration-50">
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
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group"
                            data-tip="Files">
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
                    <li v-if="accessToken">
                        <button @click="handleNavigation('groups')"
                            :class="isActive('groups') ? 'text-xrb-text-primary' : 'text-xrb-text-secondary hover:text-xrb-text-primary'"
                            class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group"
                            data-tip="Groups">
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

                    <!-- Recents -->
                    <div>
                        <span
                            class="item-inline is-drawer-close:hidden p-4 text-xrb-text-secondary flex justify-start select-none">Recents</span>
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