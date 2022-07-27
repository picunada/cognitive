<template>
  <div class="container fs-4">
    <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
      <a class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none fw-bold" href="/">Cognitive</a>
      <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
        <li><a href="/#/client-list/" class="nav-link px-5 fs-6 text-white">Client List</a></li>
      </ul>
      <div class="text-end">
        <button v-if="authorized" @click="logout"
                type="button" class="btn btn-outline-light me-2">Logout</button>
        <button v-else @click="$emit('visible', true)"
                type="button" class="btn btn-outline-light me-2">Login</button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "nav-bar",
  data() {
    return {
    }
  },
  computed: {
    authorized() {
      return this.$store.state.auth.credentials.token !== null
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/onLogout').then(() => {
        this.$router.push({path: '/'})
      })
    }
  }
};
</script>
<style>

</style>
