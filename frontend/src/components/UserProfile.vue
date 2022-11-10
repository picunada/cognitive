<script setup lang="ts">
const auth = useAuthStore()
</script>

<template>
  <div flex h-full>
    <div i-ph:user-focus-light text-40 m0 p0 />
    <div w-full h-full mt8>
      <p md:text-23px lg:text-25px>
        Email: {{ auth.user?.email }}
      </p>
      <p md:text-23px lg:text-25px>
        Name: {{ auth.user?.first_name }} {{ auth.user?.last_name }}
      </p>
      <p md:text-23px lg:text-25px>
        Role: {{ auth.user?.role }}
      </p>
    </div>
  </div>
</template>
