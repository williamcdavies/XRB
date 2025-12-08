<template>
  <div v-if="loading">
    <VueSpinner size="20" color="white" />
  </div>
  <div v-else-if="error">Error: {{ error }}</div>
  <div v-else>
    <div class="m-10 rounded-box border">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>name</th>
            <th>distance</th>
            <th>distance_err</th>
            <th>rl</th>
            <th>incl</th>
            <th>incl_err</th>
            <th>hard_line_slope</th>
            <th>hard_line_slope_err</th>
            <th>spec_type</th>
            <th>p_orb</th>
            <th>mass</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="xrb in xrbs" :key="xrb.name">
            <td>{{ xrb.name }}</td>
            <td>{{ xrb.distance }}</td>
            <td>{{ xrb.distance_err }}</td>
            <td>{{ xrb.rl }}</td>
            <td>{{ xrb.incl }}</td>
            <td>{{ xrb.incl_err }}</td>
            <td>{{ xrb.hard_line_slope }}</td>
            <td>{{ xrb.hard_line_slope_err }}</td>
            <td>{{ xrb.spec_type }}</td>
            <td>{{ xrb.p_orb }}</td>
            <td>{{ xrb.mass }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {
  VueSpinner,
} from 'vue3-spinners';

export default {
  components: {
    VueSpinner,
  },

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
        const response = await axios.get('https://xrb.unr.dev/api/xrb/')
        this.xrbs = response.data
      } catch (err) {
        this.error = err.message
        console.error('Error fetching XRBs:', err)
      } finally {
        this.loading = false
      }
    }
  },

  mounted() {
    this.fetchXRBs()
  }
}
</script>