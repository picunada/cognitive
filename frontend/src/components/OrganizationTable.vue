<script setup lang="ts">
import type { Ref } from 'vue'
import type { Organization } from '~/models/organization'

const organizationStore = useOrganizationStore()

const selectedOrganization: Ref<Organization | undefined> = ref()

const toggleModal = (organization: Organization | undefined) => {
  if (!selectedOrganization.value)
    selectedOrganization.value = organization
  else
    selectedOrganization.value = undefined
}

onMounted(async () => {
  await organizationStore.fetchOrganizations({ page: organizationStore.currentPage })
})
</script>

<template>
  <div mb5 flex justify-between items-center>
    <input v-model="organizationStore.searchQuery" animation text-field type="text" placeholder="Search ...">
    <Pagination v-model:current-page="organizationStore.currentPage" :total="organizationStore.totalPages" />
  </div>
  <div v-auto-animate grid lg:grid-cols-2 md:grid-cols-1 md:pr10 lg:pr0 gap3 w-full>
    <template v-for="organization in organizationStore.organizations" :key="organization.id">
      <div
        class="group animation cursor-pointer flex w-full h-120px max-h-120px items-center p4 bg-neutral-100 hover:bg-neutral-200 dark:bg-dark-700 dark:hover:bg-dark-800 rounded-10px"
        @click="toggleModal(organization)">
        <div i-ph:user-focus-light animation text-120px mr2 group-hover:text-sky-400 opacity-75 />
        <div w-full h-full flex flex-col justify-between>
          <div w-full h-full flex justify-between>
            <div h-full flex items-start md:text-23px lg:text-25px>
              {{ organization.name }}
            </div>
            <div flex flex-col gap2 items-end>
              <div opacity-50>
                {{ `Created:
                                ${organization.created_at.getDate()}/${organization.created_at.getMonth()}/${organization.created_at.getFullYear()}`
                }}
              </div>
              <div md:text-17px lg:text-20px>
                {{ `Count: ${organization.count ?? 0}` }}
              </div>
            </div>
          </div>
          <div w-full h-full flex justify-end items-end>
            <div w-7 h-7 icon-btn hover:text-red i-ph:trash-light
              @click.stop="organizationStore.deleteOrganization(organization.id)" />
          </div>
        </div>
      </div>
    </template>
    <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
      <template v-if="selectedOrganization">
        <OrganizationModal v-model:organization="selectedOrganization" v-model:rsakey="selectedOrganization.hashed_key"
          @update-organization="organizationStore.updateOrganization(selectedOrganization?.id, selectedOrganization)"
          @close="toggleModal(selectedOrganization)" />
      </template>
    </transition>
  </div>
</template>
