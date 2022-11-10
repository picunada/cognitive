<script setup lang="ts">
import type { LoginData } from '~/store/auth'

const auth = useAuthStore()
const loginData = ref<LoginData>({
  email: '',
  password: '',
} as LoginData)

const isValidated = computed(() => loginData.value.email.length > 0 && loginData.value.password.length > 0)
</script>

<template>
  <div flex h-full w-full items-center justify-center px10>
    <div flex flex-col w-full items-center justify-center max-w-120 bg-neutral-100 dark:bg-dark-700 gap4 rounded-12px p3>
      <h1 title2>
        Login
      </h1>
      <!-- Email -->
      <div class="group w-full">
        <p group-focus:text-sky text-13px mb1 ml2 opacity-40>
          Email
        </p>
        <input v-model="loginData.email" type="email" text-field w-full placeholder="Email">
      </div>
      <!-- Password -->
      <div class="group w-full">
        <p group-focus:text-sky text-13px mb1 ml2 opacity-40>
          Password
        </p>
        <input v-model="loginData.password" type="password" text-field w-full placeholder="Password">
      </div>
      <button :disabled="!isValidated" btn text-25px @click="auth.login(loginData)">
        Submit
      </button>
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: login
</route>
