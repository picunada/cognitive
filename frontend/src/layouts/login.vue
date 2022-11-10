<template>
  <main h-screen w-screen flex flex-col items-center text-gray-700 dark:text-gray-200>
    <Header />
    <div flex flex-1 w-full max-w-1390px>
      <div px2 pt5 w-full>
        <RouterView />
      </div>
    </div>
    <div my-5 mx-auto text-center opacity-75 dark:opacity-50 text-sm>
      @AI-House
    </div>
  </main>
</template>
