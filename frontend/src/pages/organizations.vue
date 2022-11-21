<script setup lang="ts">
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'
import type { Organization } from '~/models/organization'
import { Status } from '~/models/organization'

const organizationStore = useOrganizationStore()

const isOpen = ref<boolean>(false)
const organization = ref<Organization>({} as Organization)

const statuses = Object.values(Status) as [string]

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
        Organizations
      </h2>
      <button btn text-lg @click="openModal">
        Create organization
      </button>
    </div>

    <Suspense>
      <OrganizationTable />
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
              <form @submit.prevent="organizationStore.createOrganization(organization), closeModal()">
                <div mb3 flex flex-col gap2>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Name
                    </p>
                    <input v-model="organization.name" animation text-field w-full type="text">
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      RSA-Key
                    </p>
                    <input v-model="organization.hashed_key" animation text-field w-full type="text">
                  </div>
                  <div>
                    <p text-13px mb1 ml2 opacity-40>
                      Status
                    </p>
                    <ComboBox v-model:value="organization.status" :iterable="statuses" />
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
