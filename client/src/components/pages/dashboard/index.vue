<script setup lang="ts">
import Hero from './Hero.vue';
import Drawer from './Drawer.vue';
import AccountComponent from './content/Account.vue'
</script>


<template>
    <div class="relative min-h-screen ">
        <!-- Z0 -->
        <Hero class="absolute inset-0 z-0" />

        <!-- Z1 -->
        <div class="flex flex-row relative z-1">
            <Drawer />
            <AccountComponent />
        </div>

    </div>
</template>


<style scoped></style>