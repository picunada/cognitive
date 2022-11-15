<script setup lang="ts">
import type { User } from '~/models/user'

const props = defineProps<{
  user: User
}>()

const emit = defineEmits(['close', 'update:rsakey', 'update-organization'])
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
              {{ props.user.first_name }} {{ props.user.last_name }}
            </h1>
            <div flex items-center>
              <div i-ph:x icon-btn text-5 title="Close button" @click="emit('close')" />
            </div>
          </div>
          <!-- Email -->
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Email
            </p>
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              {{ props.user.email }}
            </div>
          </div>
          <!-- Role -->
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Role
            </p>
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              {{ props.user.role }}
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
