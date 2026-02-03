<script setup lang="ts">
  // Ref: https://vuejs.org/guide/components/events.html
  const emit = defineEmits<{
    (e: 'auth'): void
  }>()
</script>


<!-- Ref: https://daisyui.com/components/navbar/ -->
<template>
  <div class="absolute navbar h-24 px-16">
    <div class="flex-1">
      <a class="btn btn-ghost text-xl">XRB</a>
    </div>
  </div>
</template>


<style scoped>
</style>