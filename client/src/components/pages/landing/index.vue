<script setup lang="ts">
    import { ref }   from 'vue';

    // Layers
    import BlurLayer from '../../layers/BlurLayer.vue';
    import TintLayer from '../../layers/TintLayer.vue';

    // Modals
    import AuthModal from '../../modals/auth';

    import Hero      from './Hero.vue';
    import Navbar    from './Navbar.vue'
    

    const renderAuthModal = ref(false)
</script>


<template>
    <!-- Z0 -->
    <Navbar @register="renderAuthModal = true" @login="renderAuthModal = true" />
    <Hero />
    <!-- Z1 -->
    <TintLayer :visible="renderAuthModal" />
    <!-- Z2 -->
    <AuthModal :visible="renderAuthModal" @close="renderAuthModal = false" />
</template>


<style scoped>
</style>