<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import axios from 'axios';

defineOptions({
  name: 'App',
});

const isLoggedIn = ref(false)

onMounted(() => {
  checkAuthStatus()
})

function checkAuthStatus() {
  const token = localStorage.getItem('token')
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Token ${token}`
    isLoggedIn.value = true
  }
}

async function logout() {
  try {
    await axios.post('http://localhost:8080/api/logout/')
    location.reload()
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    // Clean up even if request fails
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    delete axios.defaults.headers.common['Authorization']
    isLoggedIn.value = false
  }
}
</script>

<template>
  <div class="flex flex-col w-full">
    <div class="navbar bg-black">
      <div class="flex flex-row items-center p-2 m-2 rounded-xl outline-2">
        <p class="font-bold text-4xl mr-2">UNR XRB</p>
        <svg class="w-15 fill-white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M13,8H12a3.954,3.954,0,0,0-1.323.242A6,6,0,0,1,16,5a1,1,0,0,0,0-2,8.009,8.009,0,0,0-8,8v1a3.954,3.954,0,0,0,.242,1.323A6,6,0,0,1,5,8,1,1,0,0,0,3,8a8.009,8.009,0,0,0,8,8h1a3.954,3.954,0,0,0,1.323-.242A6,6,0,0,1,8,19a1,1,0,0,0,0,2,8.009,8.009,0,0,0,8-8V12a3.954,3.954,0,0,0-.242-1.323A6,6,0,0,1,19,16a1,1,0,0,0,2,0A8.009,8.009,0,0,0,13,8Zm-1,6a2,2,0,1,1,2-2A2,2,0,0,1,12,14Zm9,6.5A1.5,1.5,0,1,1,19.5,19,1.5,1.5,0,0,1,21,20.5Zm0-17A1.5,1.5,0,1,1,19.5,2,1.5,1.5,0,0,1,21,3.5ZM3,3.5A1.5,1.5,0,1,1,4.5,5,1.5,1.5,0,0,1,3,3.5Zm3,17A1.5,1.5,0,1,1,4.5,19,1.5,1.5,0,0,1,6,20.5Z" />
        </svg>
      </div>
      <router-link to="/" class="btn btn-ghost text-2xl"
        style="text-decoration: none; color: inherit;">Home</router-link>
      <router-link to="/xrbplot" class="btn btn-ghost text-2xl" style="text-decoration: none; color: inherit;" v-if="isLoggedIn">XRB
        Plot</router-link>
      <router-link to="/lrlxplot" class="btn btn-ghost text-2xl" style="text-decoration: none; color: inherit;" v-if="isLoggedIn">LRLX
        Plot</router-link>
      <router-link to="/xrbtable" class="btn btn-ghost text-2xl" style="text-decoration: none; color: inherit;" v-if="isLoggedIn">XRB
        Table</router-link>
      <router-link to="/lrlxtable" class="btn btn-ghost text-2xl" style="text-decoration: none; color: inherit;" v-if="isLoggedIn">LRLX
        Table</router-link>
      <div class="flex-grow"></div>
      <div v-if="isLoggedIn">
        <button class="btn btn-error" @click="logout">Logout</button>
      </div>
    </div>
    <div class="flex grow justify-center">
      <router-view :isLoggedIn="isLoggedIn"/>
    </div>
  </div>

</template>