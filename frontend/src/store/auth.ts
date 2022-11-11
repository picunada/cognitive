import { acceptHMRUpdate, defineStore } from 'pinia'
import type { ComputedRef } from 'vue'
import type { User } from '~/models/user'

const BASE_URL = import.meta.env.VITE_URL

export interface LoginData {
  email: string
  password: string
}

interface TokenData {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', () => {
  /**
   * Current user with token
   */
  const accessToken = useStorage('access_token', '')
  const refreshToken = useStorage('refresh', '')
  const user = ref<User>()
  const authError = ref<string>()

  const isAuthenticated: ComputedRef<boolean> = computed(() => user.value !== undefined)

  const login = async (credentials: LoginData) => {
    await fetch(`${BASE_URL}/api/v1/login`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: JSON.stringify(credentials),
    }).then(async (response) => {
      const data = await response.json() as TokenData
      accessToken.value = data.access
      refreshToken.value = data.refresh
    }).catch(error => authError.value = error)
  }

  const fetchUser = async () => {
    await fetch(`${BASE_URL}/api/v1/user/my/`, {
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
        Accept: 'application/json',
      },
    }).then(async (response) => {
      if (response.status === 200) {
        const data = await response.json() as User
        user.value = data
      }
    }).catch(error => authError.value = error)
  }

  const logout = () => {
    user.value = undefined
    accessToken.value = undefined
    refreshToken.value = undefined
  }

  return {
    accessToken,
    refreshToken,
    isAuthenticated,
    user,
    authError,
    fetchUser,
    login,
    logout,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
