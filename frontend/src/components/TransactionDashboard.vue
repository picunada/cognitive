<script setup lang="ts">
const transactionStore = useTransactionsStore()
const auth = useAuthStore()

onMounted(async () => {
  await transactionStore.fetchTransactions({ page: transactionStore.currentPage })
})
</script>

<template>
  <div flex my5 justify-between>
    <h2 title2>Transactions</h2>
    <h2 v-if="auth.user?.organization.balance">
      Balance: {{ auth.user?.organization.balance }}
    </h2>
  </div>

  <div v-if="transactionStore.transactions" border dark:border-dark rounded-xl p4 w-full>
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
