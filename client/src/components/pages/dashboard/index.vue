<script setup lang="ts">
    import Hero from './Hero.vue';
    import Drawer from './Drawer.vue';
</script>


<template>
    <div class ="relative min-h-screen">
        <!-- Z0 -->
        <Hero class ="absolute inset-0 z-0"/>

        <!-- Z1 -->
        <Drawer class ="relative z-1"/>
    </div>
</template>


<style scoped>
</style>