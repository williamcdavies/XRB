<script setup lang="ts">
    //handle button clicks and navigation between components
    const emit = defineEmits<{
        changeView: [view: string]
    }>();

    const handleNavigation = (view: string) => {
        emit('changeView', view);
    };
</script>

<template>
    <!-- ref: https://daisyui.com/components/drawer/?lang=en, https://heroicons.com -->
    <div class="drawer sm:drawer-open md:drawer-open lg:drawer-open">
        <input id="dashboard-drawer" type="checkbox" class="drawer-toggle" />
        <div class="drawer-side is-drawer-close:overflow-visible">
            <div
                class="flex min-h-full flex-col items-start bg-xrb-background-1 is-drawer-close:w-14 is-drawer-open:w-64 border-r border-xrb-border-1 transition-[width] duration-300">
                <!-- Sidebar content here -->
                <ul class="menu w-full grow p-0">
                    <!-- Sidebar -->
                    <li>
                        <label for="dashboard-drawer" aria-label="open sidebar"
                            class="is-drawer-open:ml-auto p-4 cursor-pointer rounded-none tooltip tooltip-right tooltip-neutral group"
                            data-tip="Toggle Sidebar">
                            <!-- Sidebar toggle icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-linejoin="round"
                                stroke-linecap="round" stroke-width="1" stroke="currentColor" fill="none"
                                class="inline-block group-hover:stroke-xrb-accent-1 size-6 transition-colors duration-300">
                                <path
                                    d="M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z" />
                                <path d="M9 4v16" />
                            </svg>
                        </label>
                    </li>

                    <!-- Spacer -->
                    <div class="m-2"></div>

                    <!-- Home item -->
                    <li>
                        <button @click="handleNavigation('home')" class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Home">
                            <!-- Home icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                            </svg>

                            <span
                                class="is-drawer-close:hidden select-none transition-colors duration-200 group-hover:text-xrb-accent-1">Home</span>
                        </button>
                    </li>

                    <!-- New item -->
                    <li>
                        <button class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="New">
                            <!-- New item icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor"
                                class="group-hover:stroke-xrb-accent-1 size-6 transition-colors duration-300">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span
                                class="is-drawer-close:hidden select-none transition-colors duration-200 group-hover:text-xrb-accent-1">New</span>
                        </button>
                    </li>

                    <!-- Groups item -->
                    <li>
                        <button @click="handleNavigation('groups')" class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group" data-tip="Groups">
                            <!-- Groups icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor"
                                class="group-hover:stroke-xrb-accent-1 size-6 transition-colors duration-300">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5
                                    1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75
                                    18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                            </svg>
                            <span
                                class="is-drawer-close:hidden select-none transition-colors duration-200 group-hover:text-xrb-accent-1">Groups</span>
                        </button>
                    </li>

                    <!-- Spacer -->
                    <div class="m-2"></div>

                    <!-- Recents -->
                    <div>
                        <span
                            class="item-inline is-drawer-close:hidden p-4 text-xrb-accent-1 flex justify-start select-none">Recents</span>
                    </div>

                    <!-- Force to Bottom -->
                    <div class="mt-auto border-t-1 border-xrb-border-1">
                        <!-- Account item -->
                        <li>
                            <button @click="handleNavigation('account')" class="p-4 rounded-none tooltip tooltip-right tooltip-neutral group"
                                data-tip="Account">
                                <!-- Account icon -->
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                    stroke="currentColor"
                                    class="group-hover:stroke-xrb-accent-1 size-6 transition-colors duration-300">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 
                                    0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 
                                    9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg>
                                <span
                                    class="is-drawer-close:hidden select-none transition-colors duration-200 group-hover:text-xrb-accent-1">Account</span>
                            </button>
                        </li>
                    </div>
                </ul>
            </div>
        </div>
    </div>
</template>