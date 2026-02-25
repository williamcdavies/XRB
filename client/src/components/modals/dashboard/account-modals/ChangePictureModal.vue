<script setup lang="ts">

</script>


<template>
    <div class="fixed inset-0 flex items-center justify-center z-50" @click="$emit('close')">
        <div class="select-none relative bg-xrb-modal-background rounded-3xl min-w-[30rem] max-w-[30rem] h-[36rem] p-6 z-50 flex flex-col"
            @click.stop>
            <div class="relative flex rounded-3xl">
                <div @click="$emit('close')">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-8">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                </div>
                <h2 class="justify-center items-center text-2xl absolute left-1/2 -translate-x-1/2 whitespace-nowrap">
                    Profile Picture
                </h2>
            </div>
            <!-- add border border-xrb-border-1 if you like how it looks -->
            <div class="mt-6 rounded-xl flex-1 min-h-0 overflow-auto
            flex flex-col items-center justify-center space-y-4">
                <!-- Main Icon w/ placeholder-->
                <img class="w-48 h-48 rounded-full object-cover"
                    src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Rounded avatar">

                <!-- Smaller Icons Under It, Row 1 -->
                <div class="flex flex-row gap-4">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                </div>

                <!-- Row 2-->
                <div class="flex flex-row gap-4">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                    <img class="w-18 h-18 rounded-full object-cover"
                        src="../../../../assets/images/profile-icons/profile-icon-1.jpg" alt="Small icon">
                </div>
            </div>
            <div class="flex flex-row justify-end bottom-6 pt-6 rounded-3x gap-2 w-full">
                <div @click="$emit('close')"
                    class="hover:bg-xrb-menu-background-accent px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer text-xrb-accent-1">
                    <p>Cancel</p>
                </div>
                <div @click="$emit('save')"
                    class="bg-xrb-accent-1 px-4 py-2 rounded-3xl flex items-center justify-center cursor-pointer">
                    <p>Save</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>