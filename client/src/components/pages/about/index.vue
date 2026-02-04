<script setup lang="ts">
  import Navbar from '../landing/Navbar.vue'

  // Use existing site image; replace with your about image as needed
  import aboutImage from '../../../assets/images/xrb-crew.jpg'
</script>

<template>
  <div class="min-h-screen bg-[#080808]">
    <Navbar />

    <main class="pt-24 px-4 pb-16 max-w-3xl mx-auto">
      <figure class="flex flex-col items-center mb-12">
        <img
          :src="aboutImage"
          alt="About"
          class="w-full max-w-xl rounded-lg object-cover shadow-lg"
        />
      </figure>

      <div class="prose prose-invert prose-lg max-w-none text-center">
        <h1 class="text-3xl font-semibold text-white mb-6">About XRB</h1>
        <p class="text-white/90 leading-relaxed mb-4">
          The UNR XRB project is a collaborative research platform designed to centralize fragmented astronomical data on X-ray binary systems, which are currently scattered across numerous research papers and databases.
        </p>
        <p class="text-white/90 leading-relaxed">
          By providing astronomers with a unified system for uploading, managing, and visualizing observational data, the platform enables researchers to efficiently study fundamental relationships in black hole accretion physics, such as correlations between radio luminosity, X-ray luminosity, and black hole mass, ultimately advancing our understanding of compact objects and their relativistic jets while fostering collaboration in the astrophysics community.
        </p>
      </div>
    </main>
  </div>
</template>

<style scoped>
</style>
