import { useNotification } from '@kyvg/vue3-notification'
import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Organization } from '~/models/organization'
import type { Pagination, Statistic } from '~/models/utils'

const BASE_URL = import.meta.env.VITE_URL

export const useOrganizationStore = defineStore('organization', () => {
  /**
   * Organizations
   */

  // Auth store for obtaining token
  const auth = useAuthStore()

  const organizations = ref<Organization[]>()
  const searchQuery = ref<string>('')
  const totalPages = ref<number>(1)
  const currentPage = ref<number>(1)
  const statistic = ref<Statistic>({} as Statistic)

  const { notify } = useNotification()

  const organizationError = ref<string>()

  const fetchOrganizations = async (options: { page: number; searchQuery?: string }) => {
    await fetch(`${BASE_URL}/api/v1/organization/?search=${options.searchQuery ? options.searchQuery : ''}&page=${options.page}`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
      .then(async (response) => {
        if (response.status === 200) {
          const data = await response.json() as Pagination<Organization>
          let organizationArray = data.results as Organization[]
          organizationArray = organizationArray.map((organization) => {
            organization.created_at = new Date(organization.created_at)
            if (organization.deleted_at)
              organization.deleted_at = new Date(organization.deleted_at)
            return organization
          })
          organizations.value = organizationArray
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
      })
  }

  const fetchStatistic = async () => {
    await fetch(`${BASE_URL}/api/v1/statistic/`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
      .then(async (response) => {
        if (response.status === 200) {
          const data = await response.json() as Statistic
          statistic.value = data
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
      })
  }

  const generateKeyForOrganization = async (id: number) => {
    await fetch(`${BASE_URL}/api/v1/organization/${id}/generate_key/`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
        accept: 'application/json',
      },
    }).then(async (response) => {
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
        alert(`New key: ${await response.json()}`)
      }
    }).catch(err => organizationError.value = err)
  }

  const createOrganization = async (organization: Organization) => {
    await fetch(`${BASE_URL}/api/v1/organization/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify(organization),
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
        await fetchOrganizations({ page: currentPage.value })
      }
    }).catch(error => organizationError.value = error)
  }

  const deleteOrganization = async (id: number) => {
    await fetch(`${BASE_URL}/api/v1/organization/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
    }).then(async (response) => {
      if (response.status !== 204) {
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
        await fetchOrganizations({ page: currentPage.value })
      }
    }).catch(err => organizationError.value = err)
  }

  const updateOrganization = async (id: number, organization: Organization) => {
    await fetch(`${BASE_URL}/api/v1/organization/${id}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${auth.accessToken}`,
        'Content-Type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify(organization),
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
          await fetchOrganizations({ page: currentPage.value })
        }
      })
      .catch(err => organizationError.value = err)
  }

  watch(currentPage, async (newV) => {
    await fetchOrganizations({ page: newV })
  })

  watchDebounced(searchQuery, async (newV) => {
    currentPage.value = 1
    if (newV.length > 0)
      await fetchOrganizations({ page: currentPage.value, searchQuery: newV })
    else
      await fetchOrganizations({ page: currentPage.value })
  }, { debounce: 300, maxWait: 2000 })

  return {
    organizations,
    totalPages,
    currentPage,
    searchQuery,
    organizationError,
    statistic,
    deleteOrganization,
    fetchOrganizations,
    generateKeyForOrganization,
    createOrganization,
    updateOrganization,
    fetchStatistic
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
