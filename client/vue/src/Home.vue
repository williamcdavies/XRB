<script lang="ts" setup>
import { computed, ref, defineProps } from 'vue';
import axios from 'axios';

const createAccount = ref(false)
const username = ref('')
const password = ref('')
const passwordConfirm = ref('')
const passwordMismatch = computed(() => {
  return password.value !== passwordConfirm.value && passwordConfirm.value !== '';
})
const loggedInUser = computed(() => {
  return localStorage.getItem('username') || ''
})

defineOptions({
  name: 'Home'
})

const props = defineProps({
  isLoggedIn: Boolean
});

async function login() {
  try {
    const response = await axios.post('http://localhost:8080/api/login/', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', response.data.token)
    localStorage.setItem('username', username.value)

    // Set default header
    axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`

    console.log('Logged in successfully')
    location.reload();
  } catch (error: any) {
    console.error('Login failed:', error.response?.data)
    alert('Login failed: ' + (error.response?.data?.error || 'Unknown error'))
  }
}

async function register() {
  try {
    const response = await axios.post('http://localhost:8080/api/register/', {
      username: username.value,
      password: password.value
    })
    
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('username', username.value)

    // Set default header
    axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`

    console.log('Registered new account')
    location.reload();
  } catch (error: any) {
    console.error('Registration failed:', error.response?.data)
    alert('Registration failed: ' + (error.response?.data?.error || 'Unknown error'))
  }
}
</script>

<template>
  <div class="mt-25">
    <div v-if="isLoggedIn">
      <p class="text-5xl">Welcome, <span class="font-bold">{{ loggedInUser }}</span>!</p>
    </div>
    <div v-else-if="createAccount" class="flex flex-col items-center p-5 bg-black rounded-3xl">
      <p class="text-3xl font-bold mb-3">Create Account</p>
      <div>
        <label class="input">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </g>
          </svg>
          <input v-model="username" type="text" placeholder="Username" required />
        </label>
      </div>
      <div class="">
        <label class="input validator mt-3">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
              <path
                d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z">
              </path>
              <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
            </g>
          </svg>
          <input v-model="password" type="password" required placeholder="Password" minlength="8"
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
        </label>
        <p class="validator-hint hidden">
          Must be more than 8 characters, including
          <br />- At least one number <br />- At least one lowercase letter <br />- At least one uppercase letter
        </p>
      </div>
      <div class="mb-3">
        <label class="input mt-3">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
              <path
                d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z">
              </path>
              <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
            </g>
          </svg>
          <input v-model="passwordConfirm" type="password" required placeholder="Confirm Password" />
        </label>
        <p v-if="passwordMismatch" class="text-red-700 text-center">
          Passwords do not match!
        </p>
      </div>

      <button class="btn btn-success w-full mb-5" @click="register">Create Account</button>

      <div class="flex flex-col outline-2 p-3 rounded-2xl w-full items-center">
        <p class="italic mb-2">Already have an account?</p>
        <button class="btn btn-error w-full" @click="createAccount = false">Login</button>
      </div>
    </div>
    <div v-else class="flex flex-col items-center p-5 bg-black rounded-3xl">
      <p class="text-3xl font-bold mb-3">Login</p>
      <div>
        <label class="input">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </g>
          </svg>
          <input v-model="username" type="text" placeholder="Username" required />
        </label>
      </div>
      <div class="mb-3">
        <label class="input validator mt-3">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
              <path
                d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z">
              </path>
              <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
            </g>
          </svg>
          <input v-model="password" type="password" required placeholder="Password" minlength="8"
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
        </label>
        <p class="validator-hint hidden">
          Must be more than 8 characters, including
          <br />- At least one number <br />- At least one lowercase letter <br />- At least one uppercase letter
        </p>
      </div>

      <button class="btn btn-info w-full mb-5" @click="login">Submit</button>

      <div class="flex flex-col outline-2 p-3 rounded-2xl w-full items-center">
        <p class="italic mb-2">Need to create an account?</p>
        <button class="btn btn-error w-full" @click="createAccount = true">Create account</button>
      </div>

    </div>
  </div>
</template>