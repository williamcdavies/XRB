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
            <th>classification</th>
            <th>lr</th>
            <th>lr_ler</th>
            <th>lr_uer</th>
            <th>lx</th>
            <th>lx_ler</th>
            <th>lx_uer</th>
            <th>uplink</th>
            <th>alpha</th>
            <th>nu</th>
            <th>e1_measured</th>
            <th>e2_measured</th>
            <th>gamma</th>
            <th>time</th>
            <th>ref</th>
            <th>id</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lrlx in lrlxs" :key="lrlx.id">
            <td>{{ lrlx.name }}</td>
            <td>{{ lrlx.classification }}</td>
            <td>{{ lrlx.lr }}</td>
            <td>{{ lrlx.lr_ler }}</td>
            <td>{{ lrlx.lr_uer }}</td>
            <td>{{ lrlx.lx }}</td>
            <td>{{ lrlx.lx_ler }}</td>
            <td>{{ lrlx.lx_uer }}</td>
            <td>{{ lrlx.uplink }}</td>
            <td>{{ lrlx.alpha }}</td>
            <td>{{ lrlx.nu }}</td>
            <td>{{ lrlx.e1_measured }}</td>
            <td>{{ lrlx.e2_measured }}</td>
            <td>{{ lrlx.gamma }}</td>
            <td>{{ lrlx.time }}</td>
            <td>{{ lrlx.ref }}</td>
            <td>{{ lrlx.id }}</td>
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
      lrlxs: [],
      loading: false,
      error: null
    }
  },

  methods: {
    async fetchLRLXs() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.get('http://localhost:8080/api/lrlx/')
        this.lrlxs = response.data
        console.log('LRLXs fetched:', this.xrbs)
      } catch (err) {
        this.error = err.message
        console.error('Error fetching LRLXs:', err)
      } finally {
        this.loading = false
      }
    }
  },

  mounted() {
    this.fetchLRLXs()
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