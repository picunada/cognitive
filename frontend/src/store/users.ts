import { useNotification } from '@kyvg/vue3-notification'
import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Pagination } from '~/models/utils'
import type { User, UserRetrieve } from '~/models/user'

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

  const userError = ref<string>()

  const { notify } = useNotification()

  const fetchUsers = async (options: { page: number; searchQuery?: string; role?: string; organizationId?: string; organizationName?: string; orderingField?: string }) => {
    await fetch(`${BASE_URL}/api/v1/user/?role=${options.role ? options.role : ''}&organization__name=${options.organizationName ? options.organizationName : ''}&${options.organizationId ? `organization=${options.organizationId}` : ''}&ordering=${options.orderingField ? options.orderingField : ''}&search=${options.searchQuery ? options.searchQuery : ''}&page=${options.page ? options.page : ''}`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    }).then(async (response) => {
      if (response.status === 200) {
        const data = await response.json() as Pagination<User>
        let userArray = data.results as User[]
        userArray = userArray.map((user) => {
          user.created_at = new Date(user.created_at)
          return user
        })
        users.value = userArray
        totalPages.value = data.total_pages
      }
      else {
        const data = await response.json()
        let errorText = ''
        Object.entries(data).forEach((entry) => {
          const [k, v] = entry
          errorText += `${k}: ${v} \n`
        })
        notify({
          title: 'Error',
          type: 'error',
          text: errorText,
        })
      }
    }).catch((error) => {
      userError.value = error
      notify({
        title: 'Error',
        type: 'error',
        text: error,
      })
    })
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
    }).then(async (response) => {
      if (response.status !== 200 && response.status !== 201) {
        const data = await response.json()
        let errorText = ''
        Object.entries(data).forEach((entry) => {
          const [k, v] = entry
          errorText += `${k}: ${v} \n`
        })
        notify({
          title: 'Error',
          type: 'error',
          text: errorText,
        })
      }
      else {
        await fetchUsers({ page: currentPage.value })
      }
    }).catch((error) => {
      userError.value = error
      notify({
        title: 'Error',
        type: 'error',
        text: error,
      })
    })
  }

  const deleteUser = async (id: number) => {
    await fetch(`${BASE_URL}/api/v1/user/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
    })
      .then(async (response) => {
        if (response.status !== 200) {
          const data = await response.json()
          let errorText = ''
          Object.entries(data).forEach((entry) => {
            const [k, v] = entry
            errorText += `${k}: ${v} \n`
          })
          notify({
            title: 'Error',
            type: 'error',
            text: errorText,
          })
        }
        else {
          await fetchUsers({ page: currentPage.value })
        }
      })
      .catch((err) => {
        userError.value = err
        notify({
          title: 'Error',
          type: 'error',
          text: err,
        })
      })
  }

  const updateUser = async (id: number, user: User) => {
    user.organization = user.organization.map((org) => org.id)
    await fetch(`${BASE_URL}/api/v1/user/${id}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify(user),
    })
      .then(async (response) => {
        if (response.status !== 200) {
          const data = await response.json()
          let errorText = ''
          Object.entries(data).forEach((entry) => {
            const [k, v] = entry
            errorText += `${k}: ${v} \n`
          })
          notify({
            title: 'Error',
            type: 'error',
            text: errorText,
          })
        }
        else {
          await fetchUsers({ page: currentPage.value })
        }
      })
      .catch((err) => {
        userError.value = err
        notify({
          title: 'Error',
          type: 'error',
          text: err,
        })
      })
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

