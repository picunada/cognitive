<script setup lang="ts">
const organizationStore = useOrganizationStore()

onMounted(() => {
  organizationStore.fetchStatistic()
})
</script>

<template>
  <div>
    <h2 title2>Statistic</h2>
    <div text-20px>
      <h2>
        Organizations: {{ organizationStore.statistic.organizations }}
      </h2>
      <h2>
        Users: {{ organizationStore.statistic.users }}
      </h2>
      <h2>
        Transactions: {{ organizationStore.statistic.transactions }}
      </h2>
    </div>
  </div>
</template>
