<script setup lang="ts">
import type { Ref } from 'vue'
import type { User } from '~/models/user'

const userStore = useUsersStore()
const organizationStore = useOrganizationStore()

const selectedUser: Ref<User | undefined> = ref()
const filteredOrganization = ref<string>()
// const organizations: ComputedRef<string[] | undefined> = computed(() => organizationStore.organizations?.map(x => x.name))

const toggleModal = (organization: User | undefined) => {
  if (!selectedUser.value)
    selectedUser.value = organization
  else
    selectedUser.value = undefined
}

onMounted(async () => {
  await userStore.fetchUsers({ page: userStore.currentPage })
  await organizationStore.fetchOrganizations(organizationStore.currentPage)
})

watch(filteredOrganization, async (newV) => {
  await userStore.fetchUsers({ page: userStore.currentPage, filterQuery: newV })
})
</script>

<template>
  <div mb5 flex justify-between items-center>
    <div flex gap4 items-center>
      <input v-model="userStore.searchQuery" animation text-field type="text" placeholder="Search ...">
      <!-- <ComboBox v-if="organizations" v-model:value="filteredOrganization" :iterable="organizations as [string]" /> -->
    </div>

    <Pagination v-model:current-page="userStore.currentPage" :total="userStore.totalPages" />
  </div>
  <div v-auto-animate grid lg:grid-cols-2 md:grid-cols-1 md:pr10 lg:pr0 gap3 w-full>
    <template v-for="user in userStore.users" :key="user.id">
      <div
        class="group animation cursor-pointer flex w-full h-120px max-h-120px items-center p4 bg-neutral-100 hover:bg-neutral-200 dark:bg-dark-700 dark:hover:bg-dark-800 rounded-10px"
        @click="toggleModal(user)">
        <div i-ph:user-focus-light animation text-120px mr2 group-hover:text-sky-400 opacity-75 />
        <div w-full h-full flex flex-col justify-between>
          <div w-full h-full flex justify-between>
            <div h-full flex items-start md:text-23px lg:text-25px>
              {{ user.first_name }} {{ user.last_name }}
            </div>
            <div flex flex-col gap2 items-end>
              <div opacity-50>
                {{ `Created:
                                ${user.created_at.getDate()}/${user.created_at.getMonth()}/${user.created_at.getFullYear()}`
                }}
              </div>
            </div>
          </div>
          <div w-full h-full flex justify-end items-end>
            <div w-7 h-7 icon-btn hover:text-red i-ph:trash-light @click.stop="userStore.deleteUser(user.id)" />
          </div>
        </div>
      </div>
    </template>
    <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
      <template v-if="selectedUser">
        <UserModal v-model:user="selectedUser" @close="toggleModal(selectedUser)" />
      </template>
    </transition>
  </div>
</template>
