<script setup lang="ts">
    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'continue-with-email'): void
    }>()
</script>


<template>
    <div class="flex flex-col w-1/2 p-8 gap-8">
        <!-- Header -->
        <div class="flex flex-col gap-4">
            <span class="text-2xl font-bold">Log in or sign up</span>
        </div>
        
        <!-- Body -->
        <div class="flex flex-col gap-4">
            
            <!-- Continue w/ Google -->
            <button class="group btn btn-outline btn-disabled justify-start bg-[#080808] border-white/25 text-[#cfcfcf] hover:bg-white hover:border-white hover:text-[#181818]">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-4 w-4" src="../../../assets/icons/google.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE WITH GOOGLE</span>
            </button>
            
            <!-- Continue w/ email -->
            <button @click="emit('continue-with-email')" class="group btn btn-outline justify-start bg-transparent border-white/25 text-white hover:bg-white hover:border-white hover:text-[#181818]">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/mail.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE WITH EMAIL</span>
            </button>
            
            <!-- Horizontal divider -->
            <div class="divider text-xs">OR</div>
            
            <!-- Continue as guest -->
            <button class="group btn btn-outline justify-start bg-transparent border-white/25 text-white hover:bg-white hover:border-white hover:text-[#181818]">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/users/user_3.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE AS GUEST</span>
            </button>
            
            <!-- Continue as student -->
            <button class="group btn btn-outline justify-start bg-transparent border-white/25 text-white hover:bg-white hover:border-white hover:text-[#181818]">
                <span class="flex items-center justify-center h-full w-8">
                    <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/pencils/edit_pencil_line_1.svg" />
                </span>
                <span class="text-xs tracking-wider">CONTINUE AS STUDENT</span>
            </button>
        </div>
    </div>
</template>


<style scoped>
</style>