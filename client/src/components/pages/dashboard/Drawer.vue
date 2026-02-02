<template>
    <div class="drawer lg:drawer-open">
        <input id="dashboard-drawer" type="checkbox" class="drawer-toggle" />

        <div class="drawer-side is-drawer-close:overflow-visible">
            <div class="flex min-h-full flex-col items-start bg-xrb-background-1 is-drawer-close:w-14 is-drawer-open:w-64 border-r border-xrb-border-1">
                <!-- Sidebar content here -->
                <ul class="menu w-full grow">
                    <!-- Sidebar -->
                    <li>
                        <label for="dashboard-drawer" aria-label="open sidebar" class="btn btn-square btn-ghost is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Open Sidebar">
                            <!-- Sidebar toggle icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-linejoin="round"
                                stroke-linecap="round" stroke-width="1" stroke="currentColor"
                                class="my-1.5 inline-block size-6">
                                <path d="M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z">
                                </path>
                                <path d="M9 4v16"></path>
                                <path d="M14 10l2 2l-2 2"></path>
                            </svg>
                        </label>
                    </li>

                    <!-- Spacer -->
                    <div class="m-2"></div>

                    <!-- New item -->
                    <li>
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right p-2" data-tip="New">
                            <!-- New icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor" class="hover:xrb-accent-1 size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                            <span class="is-drawer-close:hidden">New</span>
                        </button>
                    </li>

                    <!-- Groups item -->
                    <li>
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right p-2" data-tip="Groups">
                            <!-- Groups icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                            </svg>

                            <span class="is-drawer-close:hidden">Groups</span>
                        </button>
                    </li>

                    <!-- Spacer -->
                    <div class="m-2"></div>

                    <!-- Recents -->
                    <div>
                        <span class="item-inline is-drawer-close:hidden p-2 text-xrb-accent-1 flex justify-start">Recents</span>
                    </div>

                    <!-- Account item -->
                    <li>
                        <button class="fixed bottom-3 is-drawer-close:tooltip is-drawer-close:tooltip-right p-2"
                            data-tip="Account">
                            <!-- Settings icon -->
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>

                            <span class="is-drawer-close:hidden">Account</span>
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>