<script setup lang="ts">
const props = defineProps<{
  total: number
  currentPage: number
}>()

const emit = defineEmits(['update:currentPage'])
const pageRange = computed(() => {
  const array = [...Array(props.total - 1 + 1).keys()].map(x => x + 1)
  if (props.currentPage > 2 && props.currentPage <= props.total - 2)
    return array.slice(props.currentPage - 3, props.currentPage + 2)
  else if (props.currentPage > props.total - 2)
    return array.slice(props.total - 5, props.total)
  else
    return array.slice(0, props.currentPage + 3)
})
</script>

<template>
  <div>
    <div v-if="props.total <= 5 && props.total > 1" v-auto-animate flex gap2>
      <div v-for="page in props.total" :key="page" :value="page" pagination-cell :class="[page === props.currentPage ? 'text-sky' : '']" @click="emit('update:currentPage', parseInt($event.currentTarget.getAttribute('value')))">
        {{ page }}
      </div>
    </div>
    <div v-else-if="props.total > 5" v-auto-animate flex gap2>
      <div v-if="props.currentPage > 1" pagination-cell @click="emit('update:currentPage', props.currentPage - 1)">
        <div i-ph:arrow-left />
      </div>
      <div v-for="page in pageRange" :key="page" :value="page" pagination-cell :class="[page === props.currentPage ? 'text-sky' : '']" @click="emit('update:currentPage', parseInt($event.currentTarget.getAttribute('value')))">
        {{ page }}
      </div>
      <div v-if="props.currentPage < total" pagination-cell @click="emit('update:currentPage', props.currentPage + 1)">
        <div i-ph:arrow-right />
      </div>
    </div>
  </div>
</template>
