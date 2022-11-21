<script setup lang="ts">
import type { Organization } from '~/models/organization'

const props = defineProps<{
  organization: Organization
  rsakey: string
}>()

const organizationStore = useOrganizationStore()
const org = ref(props.organization)
const emit = defineEmits(['close', 'update:rsakey', 'update-organization'])

const isEditing = ref<boolean>(false)
</script>

<template>
  <div>
    <Teleport to="body">
      <div
        class="bg-black/25 backdrop-blur-sm flex items-center justify-center w-full h-full fixed z-1 left-0 top-0 p4">
        <div w-full max-w-xl bg-white dark:bg-dark-800 opacity-100 p4 rounded-4>
          <!-- Title -->
          <div flex items-center justify-between>
            <h1 title2>
              Organization
            </h1>
            <div flex items-center>
              <div i-ph:file-arrow-down-light icon-btn text-5 mr2 title="Edit button" @click="isEditing = !isEditing" />
              <div i-ph:x icon-btn text-5 title="Close button" @click="emit('close'), isEditing = false" />
            </div>
          </div>
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Name
            </p>
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              <input v-if="isEditing" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark p0
                rounded-none v-model="org.name" />
              <p v-else break-all>
                {{ props.organization.name }}
              </p>
            </div>
          </div>
          <!-- Key -->
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              RSA Key
            </p>
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              <textarea v-if="isEditing" v-model="org.hashed_key" max-h-100 w-full resize-none bg-neutral-200
                dark:bg-dark overflow-auto />
              <p v-else break-all>
                {{ props.organization.hashed_key }}
              </p>
            </div>
          </div>
          <!-- Count -->
          <div flex flex-col mt2>
            <p text-13px mb1 ml2 opacity-40>
              Balance
            </p>
            <div p4 bg-neutral-200 dark:bg-dark rounded-2>
              <input v-if="isEditing" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark p0
                rounded-none v-model="org.balance" />
              <p v-else break-all>
                {{ props.organization.balance ?? 0 }}
              </p>
            </div>
          </div>
          <div flex justify-between mt4>
            <button btn text-lg @click="organizationStore.generateKeyForOrganization(props.organization.id)">
              Generate new api-key
            </button>
            <button v-if="isEditing" btn text-lg hover:bg-green @click="emit('update-organization', org.id, org)">
              Submit
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
