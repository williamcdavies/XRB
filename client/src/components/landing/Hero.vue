<script setup lang="ts">
    import { computed, ref } from 'vue';
    import BlurLayer from '../global/effects/BlurLayer.vue';
    import Navbar    from './Navbar.vue'
    
    const renderRegisterOverlay = ref(false)
    const renderLoginOverlay    = ref(false)
    const renderBlurLayer       = computed(() => renderRegisterOverlay.value || renderLoginOverlay.value)
</script>


<template>
    <div class="min-h-screen bg-[#121212]">
        <!-- Navbar Component -->
        <Navbar @register="renderRegisterOverlay = true" @login="renderLoginOverlay = true" />

        <!-- Main -->
        <main>
        </main>
    </div>

    <!-- BlurLayer Component -->
    <BlurLayer :visible="renderBlurLayer" />
</template>


<style scoped>
</style>