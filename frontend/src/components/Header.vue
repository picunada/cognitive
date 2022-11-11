<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'

const auth = useAuthStore()
const router = useRouter()
</script>

<template>
  <nav w-full flex justify-center text-xl py4 px5 backdrop-blur>
    <div w-full max-w-1390px flex items-center justify-between>
      <div>
        <RouterLink class="icon-btn mx-2" to="/" title="Home">
          <h1 class="text-24px font-light">
            AI-House Licensing
          </h1>
        </RouterLink>
      </div>

      <div flex items-center gap-2>
        <Menu as="div" relative inline-block text-left>
          <MenuButton v-if="auth.isAuthenticated">
            {{ auth.user?.email }}
          </MenuButton>
          <transition enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0">
            <MenuItems absolute right-0 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white
              dark:bg-dark shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none>
              <div class="px-1 py-1">
                <MenuItem v-slot="{ active }">
                <button class="group flex w-full items-center rounded-md px-2 py-2 text-sm" :class="[
                  active ? 'bg-sky-500 text-white' : 'text-dark-900 dark:text-white',
                ]" @click="auth.logout(), () => router.push('/')">
                  <div i-ph:sign-out-duotone :active="active" class="mr-2 h-5 w-5 text-white" aria-hidden="true" />
                  Logout
                </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>

        <RouterLink class="icon-btn mx-2" to="/" title="Home">
          <div i-carbon:home />
        </RouterLink>

        <button class="icon-btn mx-2 !outline-none" title="Toggle darkmode" @click="toggleDark()">
          <div i="carbon-sun dark:carbon-moon" />
        </button>

        <RouterLink class="icon-btn mx-2" to="/about" title="About">
          <div i-carbon-dicom-overlay />
        </RouterLink>

        <button v-if="$route.path !== '/login' && !auth.isAuthenticated" btn font-light @click="$router.push('/login')">
          Login
        </button>
      </div>
    </div>
  </nav>
</template>
