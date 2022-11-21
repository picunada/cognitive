<script setup lang="ts">
const router = useRouter()

onMounted(() => router.push('/dashboard'))
</script>

<template>
  <div />
</template>

<route lang="yaml">
meta:
  layout: default
</route>
