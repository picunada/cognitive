<script setup lang="ts">
const auth = useAuthStore()
const organizationStore = useOrganizationStore()
</script>

<template>
  <div w-full>
    <div>
      <div flex mb3 justify-between items-center>
        <h2 title1>
          Dashboard
        </h2>
        <div v-if="auth.user?.role === 'client' && auth.user.organization.length > 0" flex gap4 items-center>
          <div text-xl font-semibold>
            Balance: {{ auth.user?.organization[0].balance }}
          </div>
          <button btn text-lg @click="organizationStore.generateKeyForOrganization(auth.user?.organization[0].id as number)">
            Generate api-key
          </button>
        </div>
      </div>
      <UserDashboard />
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: default
  requiresAuth: true
</route>
