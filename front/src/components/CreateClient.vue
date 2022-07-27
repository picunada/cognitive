<template>
  <div @click.stop="$emit('hide', false)" class="modal modal-signin d-block py-5" tabindex="-1" role="dialog" id="ref-modal">
    <div @click.stop class="modal-dialog" role="document">
      <div class="modal-content rounded-4 shadow">
        <div class="modal-header p-5 pb-4 border-bottom-0">
          <!-- <h5 class="modal-title">Modal title</h5> -->
          <h2 class="fw-bold mb-0">Create client</h2>
          <button @click.stop="$emit('hide', false)" type="button"
                  class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body p-5 pt-0">
          <form @submit="createClient" class="">
            <div class="form-floating mb-3">
              <h4>Count</h4>
              <input v-model="request.count" type="text" class="form-control rounded-3" id="count">
            </div>
            <div class="form-floating mb-3">
              <h4>RSA Key</h4>
              <textarea v-model="request.key" class="form-control rounded-3 col-md-10" id="rsaKey" placeholder=""/>
<!--              <label for="floatingPassword">RSA Key</label>-->
            </div>
            <hr class="my-4 bg-dark">
            <div class="text-center">
              <button  class="w-50 mb-2 btn btn-lg rounded-4 btn-outline-dark" type="submit">Create</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "create-client",
  data() {
    return {
      request: {
        count: 0,
        key: ''
      }
    }
  },
  methods: {
    createClient() {
      axios.post('http://localhost:8000/client', this.request).then(() => {
        this.$router.go()
      }
      )
    }
  }
}
</script>

<style scoped>

</style>