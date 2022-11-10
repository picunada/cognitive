<script setup lang="ts">

</script>

<template>
  <div grid grid-cols-2 gap3>
    <div
      class="animation flex w-full h-120px max-h-120px items-center p4 bg-neutral-100 dark:bg-dark-700 rounded-10px"
    >
      <div animate-pulse flex w-full h-full>
        <div h90px w110px mr2 rounded-full bg-neutral200 dark:bg-dark />
        <div w-full h-full flex justify-between>
          <div flex items-start md:h23px lg:h25px w150px rounded-10 bg-neutral200 dark:bg-dark />
          <div flex flex-col gap2 items-end>
            <div h20px w100px rounded-10 bg-neutral200 dark:bg-dark />
            <div md:h17px lg:h20px w200px rounded-10 bg-neutral200 dark:bg-dark />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
