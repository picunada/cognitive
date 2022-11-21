<script setup lang="ts">
import type { ComputedRef } from 'vue'

const transactionStore = useTransactionsStore()
const organizationStore = useOrganizationStore()

const organizations: ComputedRef<string[] | undefined> = computed(() => organizationStore.organizations?.map(x => x.name))
const filteredOrganization = ref<string>()

onMounted(async () => {
  await transactionStore.fetchTransactions({ page: transactionStore.currentPage })
  await organizationStore.fetchOrganizations({ page: organizationStore.currentPage })
})

watch(filteredOrganization, async (newV) => {
  await transactionStore.fetchTransactions({ page: transactionStore.currentPage, organizationName: newV })
})
</script>

<template>
  <div flex my5 justify-between>
    <div flex gap3 items-center>
      <div relative>
        <div absolute z-10 bottom-11 left-4 opacity-50>
          Search
        </div>
        <input v-model="transactionStore.searchQuery" animation text-field type="text" placeholder="Search ...">
      </div>

      <ComboBox v-if="organizations" v-model:value="filteredOrganization" :iterable="organizations as [string]"
        header="Organization Name" />
    </div>
    <Pagination v-model:current-page="transactionStore.currentPage" :total="transactionStore.totalPages" />
  </div>

  <div border dark:border-dark rounded-xl p4 w-full>
    <div v-auto-animate grid grid-cols-1 md:pr10 lg:pr0 gap3 w-full>
      <div grid grid-cols-3 title2 text-lg>
        <div>ID</div>
        <div>Organization</div>
        <div>Created At</div>
      </div>
      <template v-for="transaction in transactionStore.transactions" :key="transaction.id">
        <div grid grid-cols-3 gap3 items-center title2 text-sm hover:bg-sky p2 rounded-lg>
          <div caption>
            {{ transaction.id }}
          </div>
          <div caption>
            {{ transaction.organization }}
          </div>
          <div caption>
            {{ transaction.created_at.toLocaleDateString() }} {{ transaction.created_at.toLocaleTimeString() }}
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
