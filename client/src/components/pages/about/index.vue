<script setup lang="ts">
  import { useRouter } from 'vue-router';

  import Navbar    from './Navbar.vue';
  import Section_1 from './Section_1.vue';


  const router = useRouter()


  async function goToLanding() {
    router.push('/')
  }
</script>


<template>
  <Navbar @goto-landing="goToLanding"/>
  <Section_1 />
</template>


<style scoped>
</style>