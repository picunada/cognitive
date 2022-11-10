<script setup lang="ts">
const auth = useAuthStore()

onMounted(async () => {
  await auth.fetchUser()
})
</script>

<template>
  <main h-screen w-screen flex flex-col items-center text-gray-700 dark:text-gray-200>
    <Header />
    <div flex flex-1 w-full max-w-1390px>
      <Menu v-if="auth.isAuthenticated" />
      <div px2 pt5 w-full>
        <RouterView />
      </div>
    </div>
    <Footer />
    <div my-5 mx-auto text-center opacity-75 dark:opacity-50 text-sm>
      [Default Layout]
    </div>
  </main>
</template>
