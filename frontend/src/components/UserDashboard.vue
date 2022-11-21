<script setup lang="ts">
const auth = useAuthStore()
</script>

<template>
  <Statistic v-if="auth.user?.role == 'administrator'" mb-5 />
  <TransactionDashboard />
</template>
