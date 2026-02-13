<script setup lang="ts">
  // Ref: https://vuejs.org/guide/components/events.html
  const emit = defineEmits<{
    (e: 'goto-landing'): void
  }>()
</script>


<!-- Ref: https://daisyui.com/components/navbar/ -->
<template>
  <div class="absolute navbar h-24 px-16">
    <div class="flex-1">
      <div class="flex-1"><button @click="emit('goto-landing')" class="btn btn-ghost text-xl">XRB</button></div>
    </div>
  </div>
</template>


<style scoped>
</style>