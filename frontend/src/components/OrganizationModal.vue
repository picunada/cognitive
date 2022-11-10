<script setup lang="ts">
import type { Organization } from '~/models/organization'

const props = defineProps<{
  organization: Organization
  rsakey: string
}>()

const emit = defineEmits(['close', 'update:rsakey'])

const isEditing = ref<boolean>(false)
</script>

<template>
  <div>
    <Teleport to="body">
      <div class="bg-dark-2/40 backdrop-blur-sm flex items-center justify-center w-full h-full fixed z-1 left-0 top-0 p4">
        <div w-full max-w-200 bg-white dark:bg-dark-800 opacity-100 p4 rounded-4>
          <!-- Title -->
          <div flex items-center justify-between>
            <h1 title2>
              {{ props.organization.name }}
            </h1>
            <div flex items-center>
              <div i-ph:file-arrow-down-light icon-btn text-5 mr2 title="Edit button" @click="isEditing = !isEditing" />
              <div i-ph:x icon-btn text-5 title="Close button" @click="emit('close')" />
            </div>
          </div>
          <!-- Key -->
          <div flex flex-col mt2>
            <p text-13px mb1 ml2 opacity-40>
              RSA Key
            </p>
            <div p4 bg-neutral-200 dark:bg-dark rounded-2>
              <textarea v-if="isEditing" :value="organization.hashed_key" h-full w-full resize-none bg-neutral-200 dark:bg-dark overflow-clip @input="emit('update:rsakey', $event.target.value)" />
              <p v-else break-all>
                {{ props.organization.hashed_key }}
              </p>
            </div>
          </div>
          <!-- Count -->
          <div flex flex-col mt2>
            <p text-13px mb1 ml2 opacity-40>
              Count
            </p>
            <div p4 bg-neutral-200 dark:bg-dark rounded-2>
              <p break-all>
                {{ props.organization.count ?? 0 }}
              </p>
            </div>
          </div>
          <div flex mt4>
            <button btn text-lg>
              Generate new api-key
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
