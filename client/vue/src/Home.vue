<script lang="ts" setup>
import { computed, ref } from 'vue';

defineOptions({
  name: 'Home'
})

const createAccount = ref(false)
const password = defineModel()
const passwordConfirm = defineModel('')
const passwordMismatch = computed(() => {
  return password.value !== passwordConfirm.value && passwordConfirm.value !== '';
})
</script>

<template>
  <div v-if="createAccount" class="flex flex-col items-center p-5 bg-black rounded-3xl">
    <p class="text-3xl font-bold mb-3">Create Account</p>
    <div>
      <label class="input validator">
        <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
            <rect width="20" height="16" x="2" y="4" rx="2"></rect>
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
          </g>
        </svg>
        <input type="email" placeholder="example@example.com" required />
      </label>
      <div class="validator-hint hidden">Enter valid email address</div>
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
        <input v-model="passwordConfirm" type="password" required placeholder="Confirm Password"/>
      </label>
      <p v-if="passwordMismatch" class="text-red-700 text-center">
        Passwords do not match!
      </p>
    </div>

    <button class="btn btn-success w-full mb-5">Create Account</button>

    <div class="flex flex-col outline-2 p-3 rounded-2xl w-full items-center">
      <p class="italic mb-2">Already have an account?</p>
      <button class="btn btn-error w-full" @click="createAccount=false">Login</button>
    </div>
  </div>
  <div v-else class="flex flex-col items-center p-5 bg-black rounded-3xl">
    <p class="text-3xl font-bold mb-3">Login</p>
    <div>
      <label class="input validator">
        <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
            <rect width="20" height="16" x="2" y="4" rx="2"></rect>
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
          </g>
        </svg>
        <input type="email" placeholder="example@example.com" required />
      </label>
      <div class="validator-hint hidden">Enter valid email address</div>
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
        <input type="password" required placeholder="Password" minlength="8"
          pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
          title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
      </label>
      <p class="validator-hint hidden">
        Must be more than 8 characters, including
        <br />- At least one number <br />- At least one lowercase letter <br />- At least one uppercase letter
      </p>
    </div>

    <button class="btn btn-info w-full mb-5">Submit</button>

    <div class="flex flex-col outline-2 p-3 rounded-2xl w-full items-center">
      <p class="italic mb-2">Need to create an account?</p>
      <button class="btn btn-error w-full" @click="createAccount=true">Create account</button>
    </div>

  </div>
</template>