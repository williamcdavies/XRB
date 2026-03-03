<script setup lang="ts">
</script>


<template>
  <transition name="fade">
    <router-view />
  </transition>
</template>


<style>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 1s;
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