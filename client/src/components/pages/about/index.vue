<script setup lang="ts">
  import Navbar    from './Navbar.vue';
  import Section_1 from './Section_1.vue';


  const router = useRouter()


  async function goToLanding() {
    router.push('/')
  }
</script>


<template>
  <div class="bg-xrb-bg-1">
    <Navbar />
    <Section_1 />
  </div>
</template>


<style scoped>
</style>