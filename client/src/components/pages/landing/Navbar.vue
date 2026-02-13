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
  <div class="absolute navbar h-24 px-16">
    <div class="flex-1"><button @click="emit('goto-landing')" class="btn btn-ghost text-xl">XRB</button></div>
    <div class="flex-none">
      <ul class="menu menu-horizontal">
        <li class="px-4"><button @click="emit('goto-about')">About</button></li>
        <li class="px-4"><button @click="emit('auth')">Sign up</button></li>
        <li class="px-4"><button @click="emit('auth')">Log in</button></li>
      </ul>
    </div>
  </div>
</template>


<style scoped>
</style>