<template>
  <div v-if="show" @click.stop="hideWindow" class="modal modal-signin d-block py-5" tabindex="-1" role="dialog"
       id="ref-modal">
    <div @click.stop class="modal-dialog" role="document">
      <div class="modal-content rounded-4 shadow">
        <div class="modal-header p-5 pb-4 border-bottom-0">
          <!-- <h5 class="modal-title">Modal title</h5> -->
          <h2 class="fw-bold mb-0">Edit client</h2>
          <button @click="hideWindow" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <hr class="my-4 bg-dark">
        <div class="modal-body p-5 pt-0">
          <form>
            <div class="form-floating mb-3">
              <h3>Count</h3>
              <input v-model="count" type="number" class="form-control-lg rounded-4 fs-4 border-dark"
                     id="floatingInput" :placeholder="currentCount">
            </div>
            <button @click="ChangeCount" class="w-50 btn btn-lg  btn-dark" type="submit">Proceed</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import session from "@/api/session";

export default {
  name: "modal-window",
  data() {
    return {
      count: ''
    }
  },
  props: {
    show: {
      type: Boolean,
      default: false
    },
    id: {
      type: Number
    },
    currentCount: {}
  },
  methods: {
    hideWindow() {
      this.$emit('update:show', false)
    },
    async ChangeCount() {
      await session.patch(`http://localhost:8000/client/count/${this.id}`, {
        count: this.count
      }, {
        headers: { 'Content-type': 'application/json; charset=UTF-8' }
      })
      this.$emit('pass_to_table', this.count)
      this.count = ''
      this.hideWindow()
    }
  }
}
</script>

<style scoped>
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