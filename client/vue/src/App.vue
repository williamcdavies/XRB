<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <!-- Display your data here -->
      <ul>
        <li v-for="xrb in xrbs" :key="xrb.name">
          {{ xrb }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      xrbs: [],
      loading: false,
      error: null
    }
  },

  methods: {
    async fetchXRBs() {
      this.loading = true
        this.error = null
        
        try {
          const response = await axios.get('http://localhost:8000/api/xrb/')
          this.xrbs = response.data
          console.log('XRBs fetched:', this.xrbs)
        } catch (err) {
          this.error = err.message
          console.error('Error fetching XRBs:', err)
        } finally {
          this.loading = false
        }
    }
  },

  mounted() {
    console.log("mounted!")
    this.fetchXRBs()
  }
}
</script>

<style>
body{
  margin: 0;
  padding: 0;
  background-color: #202020!important;
}
</style>
