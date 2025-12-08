<template>
  <div v-if="loading">
    <VueSpinner size="20" color="white" />
  </div>
  <div v-else-if="error">Error: {{ error }}</div>
  <div v-else class="flex overflow-x-auto grow">
    <div class="m-10 rounded-box border">
      <table class="table table-zebra">
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
        const response = await axios.get('https://xrb.unr.dev/api/lrlx/')
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