<script setup lang="ts">
</script>

<template>
  <div flex w-full max-w-260px pt5>
    <!-- Manager menu -->
    <div w-full flex flex-col gap-1 border-l dark:border-dark opacity-75>
      <div animation border-l pl-2 dark:border-dark opacity-75 hover:border-sky-4 hover:opacity-100 active:border-sky-4
        active:opacity-100 :active="$route.path === '/dashboard'">
        <RouterLink animation flex h-36px w-full items-center px-2 hover:text-sky-400 hover:opacity-100
          active:border-sky-4 active:opacity-100 :active="$route.path === '/dashboard'" to="/dashboard"
          title="Clients management">
          Dashboard
        </RouterLink>
      </div>
      <div animation border-l pl-2 dark:border-dark opacity-75 hover:border-sky-4 hover:opacity-100 active:border-sky-4
        active:opacity-100 :active="$route.path === '/organizations'">
        <RouterLink animation flex h-36px w-full items-center px-2 active:border-sky-4 active:opacity-100
          hover:text-sky-400 hover:opacity-100 :active="$route.path === '/organizations'" to="/organizations"
          title="Organizations management">
          Organizations
        </RouterLink>
      </div>
      <div animation border-l pl-2 dark:border-dark opacity-75 hover:border-sky-4 hover:opacity-100 active:border-sky-4
        active:opacity-100 :active="$route.path === '/users'">
        <RouterLink animation flex h-36px w-full items-center px-2 active:border-sky-4 active:opacity-100
          hover:text-sky-400 hover:opacity-100 :active="$route.path === '/users'" to="/users" title="Users management">
          Users
        </RouterLink>
      </div>
      <div animation border-l pl-2 dark:border-dark opacity-75 hover:border-sky-4 hover:opacity-100 active:border-sky-4
        active:opacity-100 :active="$route.path === '/users'">
        <RouterLink animation flex h-36px w-full items-center px-2 active:border-sky-4 active:opacity-100
          hover:text-sky-400 hover:opacity-100 :active="$route.path === '/transactions'" to="/transactions"
          title="Transactions management">
          Transactions
        </RouterLink>
      </div>
    </div>
  </div>
</template>
