<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/xrb">XRB Data</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
export default {
  name: 'App'
}
</script>

<style>
nav {
  padding: 20px;
  background-color: #333;
}

nav a {
  color: white;
  margin-right: 20px;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}
</style>