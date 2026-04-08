<script setup lang="ts">
  // Ref: https://vuejs.org/guide/components/events.html
  const emit = defineEmits<{
    (e: 'goto-landing'): void
    (e: 'goto-about'): void
    (e: 'auth'): void
  }>()
</script>


<!-- Ref: https://daisyui.com/components/navbar/ -->
<template>
  <div class="absolute navbar h-24 px-16 text-xrb-text-1 bg-xrb-bg-1 flex-nowrap">
    <div class="flex-1 flex items-center min-w-0">
      <RouterLink to="/" class="btn btn-ghost text-xl shrink-0">XRB</RouterLink>
      <ul class="menu menu-horizontal flex-nowrap">
        <li class="px-4 whitespace-nowrap"><button @click="emit('goto-about')">About</button></li>
        <li class="px-4 whitespace-nowrap"><button @click="emit('auth')">Sign up</button></li>
        <li class="px-4 whitespace-nowrap"><button @click="emit('auth')">Log in</button></li>
      </ul>
    </div>
  </div>
</template>


<style scoped>
</style>