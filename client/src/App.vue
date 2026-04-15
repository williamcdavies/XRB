<script setup lang="ts">
</script>


<template>
    <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
            <component :is="Component" :key="$route.fullPath" />
        </Transition>
    </RouterView>
</template>


<style>
    .fade-enter-active,
    .fade-leave-active {
    transition: opacity 0.2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
    opacity: 0;
    }
</style>