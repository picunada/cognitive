<script setup lang="ts">
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
  TransitionRoot,
} from '@headlessui/vue'

const props = defineProps<{
  iterable: [string]
  value: any
  header?: string
}>()

const emit = defineEmits(['update:value'])

const selectedItem = ref()

const query = ref('')

const filteredItems = computed(() =>
  query.value === ''
    ? props.iterable
    : props.iterable.filter((item) => {
      return item.toLowerCase().includes(query.value.toLowerCase())
    }),
)

watch(selectedItem, (newV) => {
  emit('update:value', newV)
})

onMounted(() => {
  selectedItem.value = ''
})
</script>

<template>
  <div>
    <Combobox v-model="selectedItem">
      <div class="relative">
        <div absolute z-10 bottom-11 left-4 opacity-50>
          {{ props.header }}
        </div>
        <div class="group relative w-full px3 text-field p0">
          <div i-ph:magnifying-glass />
          <ComboboxInput class="text-field p2 w-full" :display-value="(item) => item as string"
            @change="query = $event.target.value" />
          <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-2">
            <div i-ph:caret-down-light />
          </ComboboxButton>
        </div>
        <TransitionRoot leave="transition ease-in duration-100" leave-from="opacity-100" leave-to="opacity-0"
          @after-leave="query = ''">
          <ComboboxOptions
            class="absolute z-100 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white dark:bg-dark4 py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
            <div v-if="filteredItems.length === 0 && query !== ''"
              class="relative cursor-default select-none py-2 px-4">
              Nothing found.
            </div>

            <ComboboxOption v-slot="{ selected, active }" as="template" value="">
              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                'bg-sky text-white': active,
                'text-gray-900 dark:text-white': !active,
              }">
                <span class="animation block truncate" :class="{ 'font-medium': selected, 'font-normal': !selected }">
                  {{ 'None' }}
                </span>
                <span v-if="selected" class="animation absolute inset-y-0 left-0 flex items-center pl-3 "
                  :class="{ 'text-white': active, 'text-sky': !active }">
                  <div i-ph:check class="h-5 w-5" aria-hidden="true" />
                </span>
              </li>
            </ComboboxOption>

            <ComboboxOption v-for="item in filteredItems.slice(0, 10)" :key="item" v-slot="{ selected, active }"
              as="template" :value="item">
              <li class="relative cursor-default select-none py-2 pl-10 pr-4" :class="{
                'bg-sky text-white': active,
                'text-gray-900 dark:text-white': !active,
              }">
                <span class="animation block truncate" :class="{ 'font-medium': selected, 'font-normal': !selected }">
                  {{ item }}
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
</template>
