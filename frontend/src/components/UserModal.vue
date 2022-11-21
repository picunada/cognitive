<script setup lang="ts">
import { Roles, User } from '~/models/user'

const props = defineProps<{
  user: User
}>()

const emit = defineEmits(['close', 'update-user'])
const user = ref(props.user)

const roles = Object.values(Roles) as [string]

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
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              <input v-if="isEditing" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark p0
                rounded-none v-model="user.first_name" />
              <p v-else break-all>
                {{ props.user.first_name }}
              </p>
            </div>
          </div>
          <div flex flex-col max-h-100 mt2>
            <p text-13px mb1 ml2 opacity-40>
              Last name
            </p>
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              <input v-if="isEditing" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark p0
                rounded-none v-model="user.last_name" />
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
            <div max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              <input v-if="isEditing" text-field h-auto dark:bg-dark hover:bg-neutral-200 dark:hover:bg-dark p0
                rounded-none v-model="user.email" />
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
            <div v-else max-h-100 p4 bg-neutral-200 dark:bg-dark rounded-2>
              {{ props.user.role }}
            </div>
          </div>
          <div v-auto-animate flex justify-between mt4 h-8>
            <button v-if="isEditing" btn text-lg hover:bg-green @click="emit('update-user', user.id, user)">
              Submit
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
