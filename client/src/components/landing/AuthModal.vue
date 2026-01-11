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
            <div @click.stop class="min-h-[36rem] max-h-[36rem] min-w-[48rem] max-w-[48rem] flex flex-row bg-[#181818] rounded-xl overflow-hidden">
                <div class="w-1/2"></div>
                <div class="w-1/2">
                    <img src="../../assets/images/steve-johnson-unsplash.jpg" class="h-full w-full object-cover">
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