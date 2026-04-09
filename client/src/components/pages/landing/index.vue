<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuth } from '@/composables/auth';
import { useRouter } from 'vue-router';

import TintLayer from '../../layers/TintLayer.vue';
import AuthModal from '../../modals/auth';
import Hero from './Hero.vue';
import BlackHole from './BlackHole.vue';
import BlackHoleFirefox from './BlackHoleFirefox.vue';
import Navbar from './Navbar.vue'

const auth = useAuth();
const router = useRouter();

const renderAuthModal = ref(false)
const animationState = ref<'idle' | 'zoomed'>('idle')

const isFirefox = computed(() => {
    return typeof navigator !== 'undefined' &&
        navigator.userAgent.toLowerCase().includes('firefox');
});

// store result until animation finishes
let isAuthResult = false

async function handleAuth() {
    if (animationState.value !== 'idle') return

    isAuthResult = await auth.isAuthenticated()
    animationState.value = 'zoomed'
}

function closeModal() {
    renderAuthModal.value = false
    animationState.value = 'idle'
}

function handlePostAnimation() {
    if (animationState.value !== 'zoomed') return

    if (isAuthResult) {
        goToDashboard()
    } else {
        renderAuthModal.value = true
    }
}


async function goToLanding() {
    router.push('/')
}

async function goToAbout() {
    router.push('/about')
}

async function goToDashboard() {
    router.push('/dashboard')
}
</script>


<template>
    <div>
        <!-- Z0 -->
        <Navbar @auth="handleAuth" @goto-landing="goToLanding" @goto-about="goToAbout" />

        <Hero />

        <BlackHole v-if="!isFirefox" :state="animationState" @done="handlePostAnimation" />

        <BlackHoleFirefox v-else :state="animationState" @done="handlePostAnimation" />

        <!-- Z1 -->
        <Transition name="fade">
            <TintLayer v-if="renderAuthModal" />
        </Transition>

        <!-- Z2 -->
        <Transition name="pop">
            <AuthModal v-if="renderAuthModal" @close="closeModal" />
        </Transition>
    </div>
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

<style>
html,
body {
    overflow: hidden;
    height: 100%;
}
</style>