<script setup lang="ts">
const auth = useAuthStore()
</script>

<template>
  <div flex h-full>
    <div i-ph:user-focus-light text-35 m0 p0 />
    <div h-full flex flex-col mt5 gap3>
      <div flex grid grid-cols-2 gap5 items-center>
        <p opacity-50 md:text-23px lg:text-25p min-w-20>
          Email
        </p>
        <p md:text-23px lg:text-25p>
          {{ auth.user?.email }}
        </p>
      </div>

      <div flex grid grid-cols-2 gap5 items-center>
        <p opacity-50 md:text-23px lg:text-25p min-w-20>
          Name
        </p>
        <p md:text-23px lg:text-25px>
          {{ auth.user?.first_name }} {{ auth.user?.last_name }}
        </p>
      </div>

      <div flex grid grid-cols-2 gap5 items-center>
        <p opacity-50 md:text-23px lg:text-25p min-w-20>
          Role
        </p>
        <p md:text-23px lg:text-25px>
          {{ auth.user?.role }}
        </p>
      </div>
    </div>
  </div>
</template>
