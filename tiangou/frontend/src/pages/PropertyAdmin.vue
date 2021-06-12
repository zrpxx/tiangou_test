<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Properties</p>
        <q-select label="Category" v-model="currentCategory" :options="categories" @input="updateTable"></q-select>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="properties"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:top>
            <q-btn color="primary" :disable="loading" label="Add property" @click="addDialog = true" />
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn dense round flat color="primary" @click="onEdit(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="negative" @click="onClickDelete(props)" icon="delete" />
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
    <q-dialog v-model="addDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmitAdd"
          style="width: 400px"
        >
          <q-input
            filled
            v-model="newName"
            label="Property name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a property name']"
          />

          <div>
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
    <q-dialog v-model="editDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmitEdit"
          style="width: 400px"
        >
          <q-input
            filled
            v-model="id"
            label="Property ID *"
            disable
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a Property id']"
          />

          <q-input
            filled
            v-model="newName"
            label="Property name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a Property name']"
          />

          <div>
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteDialog" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="primary" text-color="white" />
          <span class="q-ml-sm">Are you sure to delete this property?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup/>
          <q-btn flat label="Delete anyway" color="red" v-close-popup @click="onDelete()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: "HouseList",
  data () {
    return {
      categories: [],
      categoryMap: {},
      currentCategory: '',
      properties: [],
      loading: false,
      addDialog: false,
      deleteDialog: false,
      editDialog: false,
      newName: '',
      id: '',
      deleteID: -1,
      columns: [
        {
          name: 'ID',
          required: true,
          label: 'Property ID',
          align: 'left',
          field: row => row.pid,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'Name',
          required: true,
          label: 'Property name',
          align: 'left',
          field: row => row.name,
        },
        { name: 'actions', label: 'Actions', field: '', align:'center' }
      ],
      pagination: {
        rowsPerPage: 25
      }
    }
  },
  created() {
    this.loading = true
    let _this = this
    this.$axios.get('http://tiangou.zrp.cool/api/categories').then(function (response) {
      let res = response.data
      console.log(res)
      _this.categoryMap = new Map()
      for(let i = 0; i < res.categories.length; i++) {
        _this.categoryMap.set(res.categories[i].name, res.categories[i].cid)
        _this.categories.push(
          res.categories[i].name
        )
      }
      _this.currentCategory = res.categories[0].name
      _this.updateTable()
      console.log(_this.categoryMap)
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    updateTable() {
      this.properties = []
      let _this = this
      this.$axios.get('http://tiangou.zrp.cool/api/properties/' + this.categoryMap.get(this.currentCategory)).then(function (response) {
        let res = response.data
        console.log(res)
        _this.properties = res.properties
        console.log(_this.properties)
        _this.$forceUpdate()
      })
      this.loading = false
    },
    onSubmitAdd() {
      let _this = this
      this.$axios.post('http://tiangou.zrp.cool/api/property/create', {
        category_id: _this.categoryMap.get(_this.currentCategory),
        property_name: _this.newName
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully added.'
          })
          _this.addDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Add error.' + res.message
          })
        }
      }).catch(function (error) {
        console.log(error)
        _this.$q.notify({
          type: 'negative',
          message: 'Internal error.'
        })
      })
    },
    onSubmitEdit() {
      let _this = this
      this.$axios.post('http://tiangou.zrp.cool/api/property/update', {
        property_id: _this.id,
        newName: _this.newName
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully edited.'
          })
          _this.editDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Edit error.' + res.message
          })
        }
      }).catch(function (error) {
        console.log(error)
        _this.$q.notify({
          type: 'negative',
          message: 'Internal error.'
        })
      })
    },
    onClickDelete(props) {
      this.deleteDialog = true
      this.deleteID = props.row.pid
    },
    onDelete() {
      let _this = this
      this.$axios.delete('http://tiangou.zrp.cool/api/property/delete', {
        data:{
          property_id: this.deleteID
        }
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully deleted.'
          })
          _this.deleteDialog = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Delete error.' + res.message
          })
        }
      }).catch(function (error) {
        console.log(error)
        _this.$q.notify({
          type: 'negative',
          message: 'Internal error.'
        })
      })
    },
    onEdit(props) {
      this.id = props.row.pid
      this.newName = props.row.name
      this.editDialog = true
    }
  }
}
</script>

<style scoped>
</style>
