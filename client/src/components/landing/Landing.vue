<script setup lang="ts">
    import { computed, ref } from 'vue';
    import BlurLayer from '../global/effects/BlurLayer.vue';
    import Hero      from './Hero.vue';
    import Navbar    from './Navbar.vue'
    
    const renderRegisterOverlay = ref(false)
    const renderLoginOverlay    = ref(false)
    const renderBlurLayer       = computed(() => renderRegisterOverlay.value || renderLoginOverlay.value)
</script>


<template>
    <!-- Z0 -->
    <Navbar @register="renderRegisterOverlay = true" @login="renderLoginOverlay = true" />
    <Hero />

    <!-- Z1 -->
    <BlurLayer :visible="renderBlurLayer" />
</template>


<style scoped>
</style>