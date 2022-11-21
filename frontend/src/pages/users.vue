<script setup lang="ts">
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import type { ComputedRef } from 'vue'
import type { UserCreate } from '~/models/user'
import { Roles } from '~/models/user'

const userStore = useUsersStore()
const organizationStore = useOrganizationStore()

const isOpen = ref<boolean>(false)
const user = ref<UserCreate>({} as UserCreate)
const organizations: ComputedRef<string[] | undefined> = computed(() => organizationStore.organizations?.map(x => x.name))

const roles = Object.values(Roles) as [string]

function closeModal() {
  isOpen.value = false
}
function openModal() {
  isOpen.value = true
}
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
                      Email
                    </p>
                    <input v-model="user.email" animation text-field w-full type="text">
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
                    <ComboBox v-model:value="user.organization" :iterable="organizations as [string]" />
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
