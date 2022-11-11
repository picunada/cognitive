<script setup lang="ts">
</script>

<template>
  <div w-full>
    <h2 title1 mb5>
      Profile
    </h2>
    <UserProfile />
  </div>
</template>

<route lang="yaml">
meta:
  layout: default
  requiresAuth: true
</route>
