<script setup lang="ts">
    // Ref: https://vuejs.org/guide/components/props.html
    const props = defineProps<{
        visible: boolean
    }>()

    // Ref: https://vuejs.org/guide/components/events.html
    const emit = defineEmits<{
        (e: 'close'): void
    }>()
</script>


<template>
    <Transition name="pop">
        <div v-if="visible" @click="emit('close')" class="fixed inset-0 flex items-center justify-center">
            <div @click.stop class="flex flex-row min-h-[36rem] max-h-[36rem] min-w-[48rem] max-w-[48rem] bg-[#181818] overflow-hidden rounded-xl">
                <!-- Left -->
                <div class="flex flex-col w-1/2 p-8 gap-8">
                    <!-- Header -->
                    <div>
                        <h1 class="text-2xl font-bold">Log in or sign up</h1>
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
                        <button class="group btn btn-outline justify-start bg-transparent border-white/25 text-white hover:bg-white hover:border-white hover:text-[#181818]">
                            <span class="flex items-center justify-center h-full w-8">
                                <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/mail.svg" />
                            </span>
                            <span class="text-xs tracking-wider">CONTINUE WITH EMAIL</span>
                        </button>
                        <!-- Divider -->
                        <div class="divider text-xs">OR</div>
                        <!-- Continue as guest -->
                        <button class="group btn btn-outline justify-start bg-transparent border-white/25 text-white hover:bg-white hover:border-white hover:text-[#181818]">
                            <span class="flex items-center justify-center h-full w-8">
                                <img class="h-5 w-5 group-hover:invert " src="../../../assets/icons/user_3.svg" />
                            </span>
                            <span class="text-xs tracking-wider">CONTINUE AS GUEST</span>
                        </button>
                    </div>
                    <!-- Footer -->
                    <div></div>
                </div>
                <!-- Right -->
                <div class="w-1/2">
                    <img src="../../../assets/images/steve-johnson-unsplash.jpg" class="h-full w-full object-cover">
                </div>
            </div>
        </div>
    </Transition>
</template>


<style scoped>
    .pop-enter-active, 
    .pop-leave-active {
        transition: opacity 0.33s ease, transform 0.33s ease;
    }

    .pop-enter-from, 
    .pop-leave-to {
        opacity: 0;
        transform: scale(0.75);
    }

    .pop-enter-to, 
    .pop-leave-from {
        opacity: 1;
        transform: scale(1);
    }
</style>