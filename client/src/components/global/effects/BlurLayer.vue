<script setup lang="ts">
    // Ref: https://vuejs.org/guide/components/props.html
    const props = defineProps<{
        visible: boolean
    }>()
</script>


<template>
    <Transition name="fade">
        <div v-if="visible" class="fixed inset-0 bg-black/25 backdrop-blur-[4px]"></div>
    </Transition>
</template>


<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.34s;
    }
    
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
    
    .fade-enter-to,
    .fade-leave-from {
        opacity: 1;
    }
</style>