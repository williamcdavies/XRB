<script setup lang="ts">
    import { ref }   from 'vue';
    // import BlurLayer from '../../layers/BlurLayer.vue';
    import TintLayer from '../../layers/TintLayer.vue';
    import AuthModal from '../../modals/auth';
    import Hero      from './Hero.vue';
    import Navbar    from './Navbar.vue'
    
    const renderAuthModal = ref(false)
</script>


<template>
    <!-- Z0 -->
    <Navbar @auth="renderAuthModal = true" />
    <Hero />
    
    <!-- Z1 -->
    <Transition name="fade">
        <TintLayer v-if="renderAuthModal" />
    </Transition>
    
    <!-- Z2 -->
    <Transition name="pop">
        <AuthModal v-if="renderAuthModal" @close="renderAuthModal = false" />
    </Transition>
</template>


<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.33s;
    }
    
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
    
    .fade-enter-to,
    .fade-leave-from {
        opacity: 1;
    }

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