<script setup lang="ts">

</script>


<template>
    <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
        <div class="select-none relative bg-xrb-menu-background rounded-3xl min-w-[30rem] max-w-[30rem] min-h-[36rem] max-h-[36rem] p-6 z-50"
            @click.stop>
            <div class="relative flex rounded-3xl">
                <div @click="$emit('close')">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-8">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>

                </div>
                <p class="text-2xl absolute left-1/2 -translate-x-1/2">
                    Change Name
                </p>
            </div>
            <div class="mt-10 rounded-3xl">
                <div class="relative w-full">
                    <input type="text" id="email" placeholder="First Name"
                        class="peer min-w-full border border-gray-300 rounded-md px-3 pt-5 pb-2 focus:outline-none focus:border-xrb-text-accent" />
                    <label for="First Name"
                        class="peer absolute left-3 -top-2 bg-xrb-menu-background px-1 text-sm text-xrb-text-secondary peer-focus:text-xrb-text-accent">
                        First Name
                    </label>
                </div>
            </div>
            <div class="mt-6 rounded-3xl">
                <div class="relative w-full">
                    <input type="text" id="email" placeholder="Last Name"
                        class="peer min-w-full border border-gray-300 rounded-md px-3 pt-5 pb-2 focus:outline-none focus:border-xrb-text-accent" />
                    <label for="Last Name"
                        class="peer absolute left-3 -top-2 bg-xrb-menu-background px-1 text-sm text-xrb-text-secondary peer-focus:text-xrb-text-accent">
                        Last Name
                    </label>
                </div>
            </div>
            <div class="absolute flex flex-row right-6 bottom-6 rounded-3x gap-2">
                <div @click="$emit('close')"
                    class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
                    <p>Cancel</p>
                </div>
                <div @click="$emit('close')"
                    class="bg-xrb-accent-1 px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer">
                    <p>Save</p>
                </div>
            </div>
        </div>
    </div>
</template>



<style scoped></style>