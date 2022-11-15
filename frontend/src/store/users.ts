import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Pagination } from '~/models/pagination'
import type { User } from '~/models/user'

const BASE_URL = import.meta.env.VITE_URL

export const useUsersStore = defineStore('users', () => {
  /**
   * Users
   */

  // Auth store for obtaining token
  const auth = useAuthStore()
  const users = ref<User[]>()
  const searchQuery = ref<string>('')
  const totalPages = ref<number>(1)
  const currentPage = ref<number>(1)

  const userError = ref<String>()

  const fetchUsers = async (options: { page: number; searchQuery?: string; filterQuery?: string }) => {
    let response: any
    if (searchQuery) {
      response = await fetch(`${BASE_URL}/api/v1/user/?search=${options.searchQuery}&page=${options.page}`, {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      })
    }
    else if (options.filterQuery) {
      response = await fetch(`${BASE_URL}/api/v1/user/??organization__name=${options.filterQuery}&page=${options.page}`, {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      })
    }
    else {
      response = await fetch(`${BASE_URL}/api/v1/user/?page=${options.page}`, {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      })
    }

    const data = await response.json() as Pagination<User>
    let userArray = data.results as User[]
    userArray = userArray.map((user) => {
      user.created_at = new Date(user.created_at)
      return user
    })
    users.value = userArray
    totalPages.value = data.total_pages
  }

  const createUser = async (user: User) => {
    await fetch(`${BASE_URL}/api/v1/user/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify(user),
    }).then(async () => {
      await fetchUsers({ page: currentPage.value })
    }).catch(error => userError.value = error)
  }

  const deleteUser = async (id: number) => {
    await fetch(`${BASE_URL}/api/v1/user/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
    }).then(async () => await fetchUsers({ page: currentPage.value }))
  }

  const updateUser = async (id: number, user: User) => {
    await fetch(`${BASE_URL}/api/v1/user/${id}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify(user),
    }).then(async () => await fetchUsers({ page: currentPage.value }))
  }

  watch(currentPage, async (newV) => {
    await fetchUsers({ page: newV })
  })

  watchDebounced(searchQuery, async (newV) => {
    currentPage.value = 1
    if (newV.length > 0)
      await fetchUsers({ page: currentPage.value, searchQuery: newV })
    else
      fetchUsers({ page: currentPage.value })
  }, { debounce: 500, maxWait: 1000 })

  return {
    users,
    userError,
    totalPages,
    searchQuery,
    currentPage,
    fetchUsers,
    createUser,
    deleteUser,
    updateUser,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))

