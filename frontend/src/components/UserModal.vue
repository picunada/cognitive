<script setup lang="ts">
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
  TransitionRoot,
} from '@headlessui/vue'
import type { Organization } from '~/models/organization'
import type { UserRetrieve } from '~/models/user'
import { Roles } from '~/models/user'

const props = defineProps<{
  user: UserRetrieve
}>()

const emit = defineEmits(['close', 'update-user'])
const user = ref<UserRetrieve>(props.user)
const organizationStore = useOrganizationStore()

const roles = Object.values(Roles) as [string]

const query = ref('')

const selectedOrganizations = ref<Organization[]>(props.user.organization)

const filteredItems = computed(() =>
  query.value === ''
    ? organizationStore.organizations
    : organizationStore.organizations?.filter((org) => {
      return org.name.toLowerCase().includes(query.value.toLowerCase())
    }),
)

const isEditing = ref<boolean>(false)
</script>

<template>
  <div>
    <Teleport to="body">
      <div
        class="bg-black/25 backdrop-blur-sm flex items-center justify-center w-full h-full fixed z-1 left-0 top-0 p4"
      >
        <div w-full max-w-xl bg-white dark:bg-dark-800 opacity-100 p4 rounded-4>
          <!-- Title -->
          <div flex items-center justify-between>
            <h1 title2>
              User
            </h1>
            <div flex items-center>
              <div i-ph:file-arrow-down-light icon-btn text-5 mr2 title="Edit button" @click="isEditing = !isEditing" />
              <div i-ph:x icon-btn text-5 title="Close button" @click="emit('close'), isEditing = false" />
            </div>
          </div>
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              First name
            </p>
            <div max-h-100 p3 bg-neutral-200 dark:bg-dark rounded-2>
              <input
                v-if="isEditing" v-model="user.first_name" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark
                p0 rounded-none
              >
              <p v-else break-all>
                {{ props.user.first_name }}
              </p>
            </div>
          </div>
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Last name
            </p>
            <div max-h-100 p3 bg-neutral-200 dark:bg-dark rounded-2>
              <input
                v-if="isEditing" v-model="user.last_name" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark
                p0 rounded-none
              >
              <p v-else break-all>
                {{ props.user.last_name }}
              </p>
            </div>
          </div>
          <!-- Email -->
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Email
            </p>
            <div max-h-100 p3 bg-neutral-200 dark:bg-dark rounded-2>
              <input
                v-if="isEditing" v-model="user.email" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark
                p0 rounded-none
              >
              <p v-else break-all>
                {{ props.user.email }}
              </p>
            </div>
          </div>
          <!-- Role -->
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Role
            </p>
            <ComboBox v-if="isEditing" v-model:value="user.role" :iterable="roles" />
            <div v-else max-h-100 p3 bg-neutral-200 dark:bg-dark rounded-2>
              {{ props.user.role }}
            </div>
          </div>
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Organization
            </p>
            <Combobox v-if="isEditing" v-model="user.organization" by="id" multiple nullable>
              <div class="relative">
                <div v-auto-animate class="group relative w-full px3 text-field h-auto p1">
                  <ul v-auto-animate f="user.organization.length > 0" flex flex-col mr2 gap1>
                    <li v-for="org in user.organization" :key="org.id">
                      {{ org.name }}
                    </li>
                  </ul>
                  <div i-ph:magnifying-glass />
                  <ComboboxInput
                    class="text-field p2 w-full" :display-value="(item: any) => item?.name"
                    @change="query = $event.target.value"
                  />
                  <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
                    <div i-ph:caret-down-light />
                  </ComboboxButton>
                </div>
                <TransitionRoot
                  leave="transition ease-in duration-100" leave-from="opacity-100"
                  leave-to="opacity-0" @after-leave="query = ''"
                >
                  <ComboboxOptions
                    class="absolute z-100 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white dark:bg-dark4 py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                  >
                    <div
                      v-if="filteredItems?.length === 0 && query !== ''"
                      class="relative cursor-default select-none py-2 px-4"
                    >
                      Nothing found.
                    </div>
                    <ComboboxOption
                      v-for="item in filteredItems?.slice(0, 10)" :key="item.id"
                      v-slot="{ selected, active }" as="template" :value="item"
                    >
                      <li
                        class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                          'bg-sky text-white': active,
                          'text-gray-900 dark:text-white': !active,
                        }"
                      >
                        <span
                          class="animation block truncate"
                          :class="{ 'font-medium': selected, 'font-normal': !selected }"
                        >
                          {{ item.name }}
                        </span>
                        <span
                          v-if="selected" class="animation absolute inset-y-0 left-0 flex items-center pl-3"
                          :class="{ 'text-white': active, 'text-sky': !active }"
                        >
                          <div i-ph:check class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ComboboxOption>
                  </ComboboxOptions>
                </TransitionRoot>
              </div>
            </Combobox>
            <div v-else flex max-h-100 p3 bg-neutral-200 dark:bg-dark rounded-2 gap1>
              <p v-for="item in user.organization" v-if="user.organization?.length === 1" :key="item.id">
                {{ `${item.name}` }}
              </p>
              <p v-for="(item, index) in user.organization" v-else :key="item.id">
                {{ index + 1 !== user.organization?.length ? `${item.name}, ` : `${item.name}` }}
              </p>
            </div>
          </div>
          <div v-auto-animate flex justify-end gap2 mt4 h8>
            <button
              v-if="isEditing" btn text-lg hover:bg-green
              @click="emit('update-user', user.id, user), emit('close')"
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
