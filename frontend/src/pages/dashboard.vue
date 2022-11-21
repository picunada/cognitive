<script setup lang="ts">
</script>

<template>
  <div w-full>
    <div>
      <h2 title1 mb5>
        Dashboard
      </h2>
      <UserDashboard />
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: default
  requiresAuth: true
</route>
