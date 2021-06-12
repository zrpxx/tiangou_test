<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Categories</p>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="categories"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:top>
            <q-btn color="primary" :disable="loading" label="Add category" @click="addDialog = true" />
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
            label="Category name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a category name']"
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
            label="Category ID *"
            disable
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a category id']"
          />

          <q-input
            filled
            v-model="newName"
            label="Category name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a category name']"
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
          <span class="q-ml-sm">Are you sure to delete this category?</span>
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
          label: 'Category ID',
          align: 'left',
          field: row => row.cid,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'Name',
          required: true,
          label: 'Category name',
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
      for(let i = 0; i < res.categories.length; i++) {
        _this.categories.push(
          {
            cid: res.categories[i].cid,
            name: res.categories[i].name
          }
        )
      }
      console.log(_this.categories)
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    onSubmitAdd() {
      let _this = this
      this.$axios.post('http://tiangou.zrp.cool/api/category/create', {
        name: _this.newName
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
      this.$axios.post('http://tiangou.zrp.cool/api/category/update', {
        id: _this.id,
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
      this.deleteID = props.row.cid
    },
    onDelete() {
      let _this = this
      this.$axios.delete('http://tiangou.zrp.cool/api/category/delete', {
        data:{
          id: this.deleteID
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
      this.id = props.row.cid
      this.newName = props.row.name
      this.editDialog = true
    }
  }
}
</script>

<style scoped>
</style>
