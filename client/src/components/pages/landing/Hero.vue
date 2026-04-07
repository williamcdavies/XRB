<script setup lang="ts">
const COUNT = 500

const stars = Array.from({ length: COUNT }, () => ({
  x: Math.random() * 100,        // percent
  y: Math.random() * 100,        // percent
  r: Math.random() * 1.4 + 0.3, // px
  opacity: Math.random() * 0.5 + 0.3,
}))
</script>

<template>
  <div class="hero min-h-screen">
    <div
      v-for="(star, i) in stars"
      :key="i"
      class="star"
      :style="{
        left: `${star.x}%`,
        top: `${star.y}%`,
        width: `${star.r * 2}px`,
        height: `${star.r * 2}px`,
        opacity: star.opacity,
    }"
    />
  </div>
</template>

<style scoped>
.hero {
  background: transparent;
  position: flex;
  overflow: hidden;
}

.star {
  position: absolute;
  border-radius: 50%;
  background: #fff;
}
</style>