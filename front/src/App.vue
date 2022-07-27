<template>
  <header class="p-3 bg-dark">
    <nav-bar @visible="(v) => {show = v}"/>
  </header>

  <body>
    <router-view></router-view>
    <log-in v-if="show" @hide="(v) => {show = v}"></log-in>
  </body>
</template>

<script>

import LogIn from "@/components/Login";
export default {
  name: "App",
  components: {
    LogIn
  },
  data () {
    return {
      show: false,
    }
  },
  methods: {
  },
};
</script>

<style>
#app {

}

body {
  height: 100vh;
}
</style>
