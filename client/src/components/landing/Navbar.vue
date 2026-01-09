<script setup lang="ts">
  // Ref: https://vuejs.org/guide/components/events.html
  const emit = defineEmits<{
    (e: 'register'): void
    (e: 'login'): void
  }>()
</script>


<!-- Ref: https://daisyui.com/components/navbar/ -->
<template>
  <div class="absolute navbar h-24 px-16">
    <div class="flex-1">
      <a class="btn btn-ghost text-xl">XRB</a>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal">
        <li class="px-4"><button @click="emit('register')">Sign up</button></li>
        <li class="px-4"><button @click="emit('login')">Log in</button></li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
</style>