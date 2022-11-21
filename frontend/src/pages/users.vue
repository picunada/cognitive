<script setup lang="ts">
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'

import type { UserCreate } from '~/models/user'
import { Roles } from '~/models/user'

const userStore = useUsersStore()
const organizationStore = useOrganizationStore()

const isOpen = ref<boolean>(false)
const user = ref<UserCreate>({
  first_name: '',
  last_name: '',
  password: '',
  confirm_password: '',
  organization: [] as number[]
} as UserCreate)

const selectedOrganization = ref()
const query = ref('')

const filteredItems = computed(() =>
  query.value === ''
    ? organizationStore.organizations
    : organizationStore.organizations?.filter((org) => {
      return org.name.toLowerCase().includes(query.value.toLowerCase())
    }),
)

const roles = Object.values(Roles) as [string]

function closeModal() {
  isOpen.value = false
}
function openModal() {
  isOpen.value = true
}

watch(selectedOrganization, (newV) => {
  if (user.value.organization.length > 0)
    user.value.organization.pop()
  user.value.organization.push()
})
</script>

<template>
  <div w-full>
    <div flex justify-between items-center mb3>
      <h2 title1>
        Users
      </h2>
      <button btn text-lg @click="openModal">
        Create user
      </button>
    </div>
    <Suspense>
      <UsersTable />
      <template #fallback>
        <TableLoading />
      </template>
    </Suspense>
  </div>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-10" @close="closeModal">
      <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
        leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-black bg-opacity-25 backdrop-blur-sm" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95">
            <DialogPanel
              class="w-full max-w-xl transform rounded-10px bg-white dark:bg-dark-800  p4 text-left align-middle shadow-xl transition-all">
              <DialogTitle as="h3" title2 mb3>
                Create organization
              </DialogTitle>
              <form @submit.prevent="userStore.createUser(user), closeModal()">
                <div mb3 flex flex-col gap2>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      First name
                    </p>
                    <input v-model="user.first_name" animation text-field w-full type="text">
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Last name
                    </p>
                    <input v-model="user.last_name" animation text-field w-full type="text">
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Role
                    </p>
                    <ComboBox v-model:value="user.role" :iterable="roles" />
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Organization
                    </p>
                    <Combobox v-model="user.organization" multiple>
                      <div class="relative">
                        <div class="group relative w-full px3 text-field p0">
                          <div i-ph:magnifying-glass />
                          <ComboboxInput class="text-field p2 w-full" :display-value="(item: any) => item as string"
                            @change="query = $event.target.value" />
                          <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
                            <div i-ph:caret-down-light />
                          </ComboboxButton>
                        </div>
                        <TransitionRoot leave="transition ease-in duration-100" leave-from="opacity-100"
                          leave-to="opacity-0" @after-leave="query = ''">
                          <ComboboxOptions
                            class="absolute z-100 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white dark:bg-dark4 py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                            <div v-if="filteredItems?.length === 0 && query !== ''"
                              class="relative cursor-default select-none py-2 px-4">
                              Nothing found.
                            </div>

                            <ComboboxOption v-slot="{ selected, active }" as="template" value="">
                              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                                'bg-sky text-white': active,
                                'text-gray-900 dark:text-white': !active,
                              }">
                                <span class="animation block truncate"
                                  :class="{ 'font-medium': selected, 'font-normal': !selected }">
                                  {{ 'None' }}
                                </span>
                                <span v-if="selected"
                                  class="animation absolute inset-y-0 left-0 flex items-center pl-3 "
                                  :class="{ 'text-white': active, 'text-sky': !active }">
                                  <div i-ph:check class="h-5 w-5" aria-hidden="true" />
                                </span>
                              </li>
                            </ComboboxOption>

                            <ComboboxOption v-for="item in filteredItems?.slice(0, 10)" :key="item.id"
                              v-slot="{ selected, active }" as="template" :value="item.id">
                              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                                'bg-sky text-white': active,
                                'text-gray-900 dark:text-white': !active,
                              }">
                                <span class="animation block truncate"
                                  :class="{ 'font-medium': selected, 'font-normal': !selected }">
                                  {{ item.name }}
                                </span>
                                <span v-if="selected" class="animation absolute inset-y-0 left-0 flex items-center pl-3"
                                  :class="{ 'text-white': active, 'text-sky': !active }">
                                  <div i-ph:check class="h-5 w-5" aria-hidden="true" />
                                </span>
                              </li>
                            </ComboboxOption>
                          </ComboboxOptions>
                        </TransitionRoot>
                      </div>
                    </Combobox>
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Email
                    </p>
                    <input v-model="user.email" animation text-field w-full type="text">
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Password
                    </p>
                    <input v-model="user.password" animation text-field w-full type="password">
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Confirm password
                    </p>
                    <input v-model="user.confirm_password" animation text-field w-full type="password">
                  </div>
                </div>

                <div flex justify-between mt5 gap2>
                  <input type="submit" value="Submit" btn text-lg>
                  <button type="button" btn text-lg @click="closeModal">
                    Close
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<route lang="yaml">
meta:
  layout: default
  requiresAuth: true
  roles:
    - administrator
    - manager
</route>
