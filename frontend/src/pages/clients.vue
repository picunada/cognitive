<script setup lang="ts">
</script>

<template>
  <div w-full>
    <h2 title1 mb-5>
      Clients
    </h2>
    <Suspense>
      <ClientTable />
      <template #fallback>
        <TableLoading />
      </template>
    </Suspense>
  </div>
</template>
