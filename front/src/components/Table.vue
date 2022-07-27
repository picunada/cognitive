<template>
  <div class="row h-100 p-5 justify-content-center">
    <div class="h-100 w-90 p-5 text-bg-dark rounded-4 ">
      <table class="table table-dark table-stripped">
        <thead>
        <tr>
          <th v-for="field in fields" :key="field" @click="sortTable(field)">
            {{ field }}<i class="bi bi-sort-alpha-down" aria-label="Sort Icon"></i>
          </th>
          <th>
            Actions
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in dataList" :key="item">
          <td v-for="field in fields" :key="field">{{ item[field].length == 0 ? 'Not defined' : item[field]}}</td>
          <td>
            <div class="btn-group">
              <button @click="showEdit(item)" type="button" class="btn btn-light text-wrap mr-5"
                      data-toggle="modal">Edit</button>
              <button v-if="item.status == 'active'" @click="blockClient(item)"
                      type="button" class="btn btn-light text-wrap mr-5">Block</button>
              <button v-else @click="unblockClient(item)" type="button" class="btn btn-light text-wrap mr-5">Unblock</button>
              <button @click="genereateApiKey(item)" type="button" class="btn btn-light text-wrap">Key</button>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
      <button @click="show = true" type="button" class="btn btn-light text-wrap">Create Client</button>
    </div>
  </div>
  <modal-window @pass_to_table="changeCount" v-model:id="currentItem.id"
                v-model:currentCount="currentItem.count"  v-model:show="editVisible"></modal-window>
  <create-client  v-if="show" @hide="(v) => {show = v}"></create-client>



</template>

<script>
import session from "@/api/session";
import CreateClient from "@/components/CreateClient";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "tableForm",
  components: {CreateClient},
  data() {
    return {
      editVisible: false,
      currentItem: {},
      show: false
    }
  },
  props: {
    fields: Array,
    dataList: Array,
  },
  methods: {
    showEdit(item) {
      this.editVisible = true
      this.currentItem = item
    },
    changeCount(count) {
      this.currentItem.count = count
    },
    async blockClient(item) {
      await session.patch(`http://localhost:8000/client/block_client/${item.id}`).then(response => {
        item.status = response.data.status
      })
    },
    async unblockClient(item) {
      await session.patch(`http://localhost:8000/client/unblock_client/${item.id}`).then(response => {
        item.status = response.data.status
      })
    },
    async genereateApiKey(item) {
      await session.get(`http://localhost:8000/client/api_key/${item.id}`).then(response => {
        item.api_key = response.data.api_key
      })
    }
  }
};
</script>