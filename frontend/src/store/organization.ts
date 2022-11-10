import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Organization } from '~/models/organization'
import type { Pagination } from '~/models/pagination'

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

  const fetchOrganizations = async (page: number, searchQuery?: string) => {
    let response: any
    if (searchQuery) {
      response = await fetch(`${BASE_URL}/api/v1/organization/?search=${searchQuery}&page=${page}`, {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      })
    }
    else {
      response = await fetch(`${BASE_URL}/api/v1/organization/?page=${page}`, {
        headers: {
          Authorization: `Bearer ${auth.accessToken}`,
        },
      })
    }

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

  const generateKeyForOrganization = async (id: string) => {
    const response = await fetch(`${BASE_URL}/api/v1/organization/${id}/generate_key`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
        accept: 'application/json',
      },
    })
    return await response.json()
  }

  watch(currentPage, async (newV) => {
    await fetchOrganizations(newV)
  })

  watchDebounced(searchQuery, async (newV) => {
    currentPage.value = 1
    if (newV.length > 0)
      await fetchOrganizations(currentPage.value, newV)
    else
      fetchOrganizations(currentPage.value)
  }, { debounce: 500, maxWait: 1000 })

  return {
    organizations,
    totalPages,
    currentPage,
    searchQuery,
    fetchOrganizations,
    generateKeyForOrganization,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
