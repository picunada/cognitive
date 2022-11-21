import { useNotification } from '@kyvg/vue3-notification'
import { acceptHMRUpdate, defineStore } from 'pinia'
import type { Transaction } from '~/models/transaction'
import type { Pagination } from '~/models/utils'

const BASE_URL = import.meta.env.VITE_URL

export const useTransactionsStore = defineStore('transactions', () => {
  const auth = useAuthStore()
  const transactions = ref<Transaction[]>()
  const userTransaction = ref<Transaction[]>()
  const searchQuery = ref<string>('')
  const totalPages = ref<number>(1)
  const currentPage = ref<number>(1)

  const { notify } = useNotification()

  const fetchTransactions = async (options: { page: number; searchQuery?: string; role?: string; organizationId?: string; organizationName?: string; orderingField?: string }) => {
    await fetch(`${BASE_URL}/api/v1/transaction/?organization__name=${options.organizationName ? options.organizationName : ''}&search=${options.searchQuery ? options.searchQuery : ''}&page=${options.page ? options.page : ''}`, {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    }).then(async (response) => {
      if (response.status === 200) {
        const data = await response.json() as Pagination<Transaction>
        let array = data.results as Transaction[]
        array = array.map((transaction) => {
          transaction.created_at = new Date(transaction.created_at)
          return transaction
        })
        transactions.value = array
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
      notify({
        title: 'Error',
        type: 'error',
        text: error,
      })
    })
  }

  return {
    transactions,
    searchQuery,
    totalPages,
    currentPage,
    userTransaction,
    fetchTransactions,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))

