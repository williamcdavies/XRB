<template>
  <div>
    <div v-if="loading">
      <VueSpinner size="20" color="white"/>
    </div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <table>
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
          const response = await axios.get('http://localhost:8080/api/xrb/')
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
    this.fetchXRBs()
  }
}
</script>

<style scoped>
body{
  margin: 0;
  padding: 0;
  background-color: #202020!important;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #2a2a2a;
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);

  display: block;
  overflow-x: auto;
  white-space: nowrap;
}

thead {
  background-color: #1a1a1a;
  position: sticky;
  top: 0;
  z-index: 10;
}

th {
  padding: 16px 12px;
  text-align: center;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #4a4a4a;
  color: #e0e0e0;
}

td {
  padding: 14px 12px;
  border-bottom: 1px solid #3a3a3a;
  font-size: 14px;
}

/* Zebra striping */
tbody tr:nth-child(odd) {
  background-color: #2a2a2a;
}

tbody tr:nth-child(even) {
  background-color: #333333;
}

/* Handle null/empty values */
td:empty::after {
  content: '—';
  color: #666;
}

/* Loading and error states */
div {
  color: #e0e0e0;
  padding: 20px;
  text-align: center;
  font-size: 18px;
}
</style>