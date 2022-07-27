<template>
  <div @click.stop="$emit('hide', false)" class="modal modal-signin d-block py-5" tabindex="-1" role="dialog" id="ref-modal">
    <div @click.stop class="modal-dialog" role="document">
      <div class="modal-content rounded-4 shadow">
        <div class="modal-header p-5 pb-4 border-bottom-0">
          <!-- <h5 class="modal-title">Modal title</h5> -->
          <h2 class="fw-bold mb-0">Login</h2>
          <button @click.stop="$emit('hide', false)" type="button"
                  class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body p-5 pt-0">
          <form @submit="login" class="">
            <div class="form-floating mb-3">
              <input v-model="user.email" type="email" class="form-control rounded-3" id="floatingInput" placeholder="name@example.com">
              <label for="floatingInput">Email address</label>
            </div>
            <div class="form-floating mb-3">
              <input v-model="user.password" type="password" class="form-control rounded-3" id="floatingPassword" placeholder="Password">
              <label for="floatingPassword">Password</label>
            </div>
            <hr class="my-4 bg-dark">
            <div class="text-center">
              <button  class="w-50 mb-2 btn btn-lg rounded-4 btn-outline-dark" type="submit">Login</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: "log-in",
  components: {},
  data() {
    return {
      user: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    login() {
      this.$store.dispatch('auth/onLogin', this.user).then(() => {
        this.$router.push({path: '/client-list'})
        this.$emit('hide', false)
      })
    }
  }
};
</script>

<style>
#login {
  color: #222;
}
#ref-modal {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  transition: opacity 0.3s ease;
}

</style>