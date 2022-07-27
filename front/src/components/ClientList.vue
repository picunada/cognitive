<template>
  <div v-if="authorized" class="text-center">
    <Table :fields="clientKeys" :dataList="clients"/>
  </div>
</template>

<script>
import Table from "./Table.vue";
import session from "@/api/session";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "ClientList",
  components: {
    Table
  },
  data () {
    return {
      clients: [],
      clientKeys: []
    }
  },
  methods: {
    async fetchData() {
      session.get("http://localhost:8000/client").then((response) => {
      response.data.forEach(item => {
        if (item.api_key.length != 0) {
          item.api_key = item.api_key[0].api_key
        }
      })
      this.clients = response.data
      const keys = Object.keys(response.data[0])
      keys.splice(keys.indexOf('key'), 1)
      this.clientKeys = keys
  })}
  },
  computed: {
    authorized() {
      return this.$store.state.auth.credentials.token !== null
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped>
</style>