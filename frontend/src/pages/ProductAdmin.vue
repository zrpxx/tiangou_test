<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Products</p>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="products"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:top>
            <q-btn color="primary" :disable="loading" label="Add product" @click="addDialog = true" />
          </template>
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn dense round flat color="primary" @click="onEdit(props)" icon="edit"></q-btn>
              <q-btn dense round flat color="primary" @click="onSetProperty(props)" icon="more"></q-btn>
              <q-btn dense round flat color="primary" @click="onSetImage(props)" icon="image"></q-btn>
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
            label="Product name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product name']"
          />

          <q-input
            filled
            v-model="newSubtitle"
            label="Product subtitle *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product subtitle']"
          />

          <q-input
            filled
            v-model="newOriginalPrice"
            label="Product original price *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product original price']"
          />

          <q-input
            filled
            v-model="newPromotePrice"
            label="Product promote *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product promote name']"
          />

          <q-input
            filled
            v-model="newStock"
            type="number"
            label="Product stock *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a stock',
                      val => val && val >= 0 || 'Please type a valid stock'
                    ]"
          />

          <q-file filled bottom-slots v-model="newThumbnail" label="Thumbnail picture *" counter
                  accept=".jpg, image/*"
                  @rejected="onImgRejected"
                  lazy-rules
                  :rules="[ val => val || 'Please upload a product thumbnail picture']">
            <template v-slot:prepend>
              <q-icon name="cloud_upload" @click.stop />
            </template>
            <template v-slot:append>
              <q-icon name="close" @click.stop="newThumbnail = null" class="cursor-pointer" />
            </template>
          </q-file>

          <q-select
            filled
            v-model="newCategory"
            label="Product category *"
            :options="categories"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a stock']"
          />
          <div class="q-mt-lg">
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
            label="Product ID *"
            disable
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product id']"
          />

          <q-input
            filled
            v-model="newName"
            label="Product name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product name']"
          />

          <q-input
            filled
            v-model="newSubtitle"
            label="Product subtitle *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product subtitle']"
          />

          <q-input
            filled
            v-model="newOriginalPrice"
            label="Product original price *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product original price']"
          />

          <q-input
            filled
            v-model="newPromotePrice"
            label="Product promote *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a product promote name']"
          />

          <q-input
            filled
            v-model="newStock"
            type="number"
            label="Product stock *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a stock',
                      val => val && val >= 0 || 'Please type a valid stock'
                    ]"
          />

          <q-select
            filled
            v-model="newCategory"
            label="Product category *"
            :options="categories"
            disable
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a stock']"
          />

          <div>
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
      </q-card>
    </q-dialog>
    <q-dialog v-model="setImg" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmitSetImg"
          style="width: 400px"
        >
          <q-file filled bottom-slots v-model="newThumbnail" label="Thumbnail picture *" counter
                  accept=".jpg, image/*"
                  @rejected="onImgRejected"
          >
            <template v-slot:prepend>
              <q-icon name="cloud_upload" @click.stop />
            </template>
            <template v-slot:append>
              <q-icon name="close" @click.stop="newThumbnail = null" class="cursor-pointer" />
            </template>
          </q-file>

          <q-img
            v-if="thumbnail_pic !== 'N/A'"
            :src="thumbnail_pic"
            style="max-width: 300px"
            class="q-mb-lg"
          >
            <div class="absolute-bottom text-subtitle1 text-center">
              Current thumbnail picture
            </div>
          </q-img>

          <q-file filled bottom-slots v-model="newDetail" label="Detail picture *" counter
                  accept=".jpg, image/*"
                  @rejected="onImgRejected"
          >
            <template v-slot:prepend>
              <q-icon name="cloud_upload" @click.stop />
            </template>
            <template v-slot:append>
              <q-icon name="close" @click.stop="newDetail = null" class="cursor-pointer" />
            </template>
          </q-file>

          <q-img
            v-if="detail_pic !== 'N/A'"
            :src="detail_pic"
            style="max-width: 300px"
            class="q-mb-lg"
          >
            <div class="absolute-bottom text-subtitle1 text-center">
              Current detail picture
            </div>
          </q-img>

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
          <span class="q-ml-sm">Are you sure to delete this product?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup/>
          <q-btn flat label="Delete anyway" color="red" v-close-popup @click="onDelete()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="setPropertyDialog" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmitSetProperty"
          style="width: 400px"
        >
          <q-input
            filled
            v-for="(property, index) in properties"
            :key="index"
            v-model="newProperty[property]"
            :label="property"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type ' + property]"
          />
          <div>
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Close" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
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
      properties: [],
      propertyMap: {},
      newProperty: {},
      products: [],
      loading: false,
      addDialog: false,
      deleteDialog: false,
      editDialog: false,
      setImg: false,
      setPropertyDialog: false,
      newThumbnail: null,
      newDetail: null,
      thumbnail_pic: 'N/A',
      detail_pic: 'N/A',
      newName: '',
      newSubtitle: '',
      newCategory: '',
      newOriginalPrice: '',
      newPromotePrice: '',
      newStock: '',
      id: '',
      deleteID: -1,
      columns: [
        {
          name: 'ID',
          required: true,
          label: 'Product ID',
          align: 'left',
          field: row => row.id,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'Name',
          required: true,
          label: 'Product name',
          align: 'left',
          field: row => row.name,
        },
        {
          name: 'Subtitle',
          required: true,
          label: 'Product subtitle',
          align: 'left',
          field: row => row.subtitle,
        },
        {
          name: 'Original price',
          required: true,
          label: 'Product original price',
          align: 'left',
          field: row => row.original_price,
          format: val => `¥${val}`,
        },
        {
          name: 'Promote price',
          required: true,
          label: 'Product promote price',
          align: 'left',
          field: row => row.promote_price,
          format: val => `¥${val}`,
        },
        {
          name: 'Stock',
          required: true,
          label: 'Product stock',
          align: 'left',
          field: row => row.stock,
        },
        {
          name: 'Create date',
          required: true,
          label: 'Product create time',
          align: 'left',
          field: row => row.create_date,
          sortable: true
        },
        {
          name: 'Category',
          required: true,
          label: 'Product category',
          align: 'left',
          field: row => this.categoryMap.get(row.category_id)
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
    this.$axios.get('http://127.0.0.1:8000/api/categories').then(function (response) {
      let res = response.data
      console.log(res)
      _this.categoryMap = new Map()
      for(let i = 0; i < res.categories.length; i++) {
        _this.categoryMap.set(res.categories[i].cid, res.categories[i].name)
        _this.categoryMap.set(res.categories[i].name, res.categories[i].cid)
        _this.categories.push(
          res.categories[i].name
        )
      }
      console.log(_this.categoryMap)
      _this.$forceUpdate()
    })
    this.$axios.get('http://127.0.0.1:8000/api/products').then(function (response) {
      let res = response.data
      console.log(res)
      _this.products = res.products
      console.log(_this.products)
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    onSubmitAdd() {

      let _this = this

      let reader = new FileReader()
      reader.onload = function () {
        console.log(reader.result)
        _this.$axios.post('http://127.0.0.1:8000/api/product/create', {
          category_id: _this.categoryMap.get(_this.newCategory),
          product_name: _this.newName,
          product_subtitle: _this.newSubtitle,
          original_price: _this.newOriginalPrice,
          promote_price: _this.newPromotePrice,
          product_stock: _this.newStock,
          thumbnail_pic: reader.result
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
      }

      reader.readAsDataURL(this.newThumbnail);
    },
    onSubmitEdit() {
      let _this = this

        _this.$axios.post('http://127.0.0.1:8000/api/product/update', {
          product_id: _this.id,
          product_name: _this.newName,
          product_subtitle: _this.newSubtitle,
          original_price: _this.newOriginalPrice,
          promote_price: _this.newPromotePrice,
          product_stock: _this.newStock
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
      this.deleteID = props.row.id
    },
    onDelete() {
      let _this = this
      this.$axios.delete('http://127.0.0.1:8000/api/product/delete', {
        data:{
          product_id: this.deleteID
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
      this.id = props.row.id
      this.newName = props.row.name
      this.newSubtitle = props.row.subtitle
      this.newCategory = this.categoryMap.get(props.row.category_id)
      this.newOriginalPrice = props.row.original_price
      this.newPromotePrice = props.row.promote_price
      this.newStock = props.row.stock
      this.editDialog = true
    },
    onSetImage(props) {
      this.id = props.row.id
      this.newDetail = null
      this.newThumbnail = null
      let _this = this
      this.$axios.get('http://127.0.0.1:8000/api/product/' + this.id).then(function (response) {
          let res = response.data
          _this.thumbnail_pic = res.thumbnail_pic
          _this.detail_pic = res.detail_pic
          _this.setImg = true
      })
    },
    onImgRejected() {
      this.$q.notify({
        type: 'negative',
        message: 'Error, file is not a image.'
      })
    },
    onSubmitSetImg() {
      if(this.newDetail !== null)
      {
        let _this = this

        let reader = new FileReader()

        reader.onload = function () {
          console.log(reader.result)
          _this.$axios.post('http://127.0.0.1:8000/api/product_image/update', {
            product_id: _this.id,
            detail: reader.result
          }).then(function (response) {
            console.log(response)
            let res = response.data
            if(res.status === 'Success') {
              _this.$q.notify({
                type: 'positive',
                message: 'Successfully edited image.'
              })
              _this.setImg = false
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
        }

        reader.readAsDataURL(this.newDetail);
      }
      if(this.newThumbnail !== null) {
        let _this = this

        let reader = new FileReader()

        reader.onload = function () {
          console.log(reader.result)
          _this.$axios.post('http://127.0.0.1:8000/api/product_image/update', {
            product_id: _this.id,
            thumbnail: reader.result
          }).then(function (response) {
            console.log(response)
            let res = response.data
            if(res.status === 'Success') {
              _this.$q.notify({
                type: 'positive',
                message: 'Successfully edited image.'
              })
              _this.setImg = false
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
        }

        reader.readAsDataURL(this.newThumbnail);
      }
    },
    onSetProperty(props) {
      this.id = props.row.id
      this.propertyMap = new Map()
      this.newProperty = {}
      this.properties = []
      let _this = this
      this.$axios.get('http://127.0.0.1:8000/api/properties/' + props.row.category_id).then(function (response) {
        let res = response.data
        console.log(res)
        for(let i = 0; i < res.properties.length; i++) {
          _this.properties.push(res.properties[i].name)
          _this.propertyMap.set(res.properties[i].name, res.properties[i].pid)
        }
        console.log(_this.properties)
        _this.setPropertyDialog = true
      })
    },
    onSubmitSetProperty() {
      let _this = this

      for(let key in this.newProperty) {
        this.$axios.post('http://127.0.0.1:8000/api/product_property/update',{
          product_id: _this.id,
          property_id: _this.propertyMap.get(key),
          value: _this.newProperty[key]
        }).then(function (response) {
          console.log(response)
          let res = response.data
          if(res.status === 'Success') {
            _this.$q.notify({
              type: 'positive',
              message: 'Successfully updated product property.'
            })
          } else {
            _this.$q.notify({
              type: 'negative',
              message: 'Update error.' + res.message
            })
          }
        }).catch(function (error) {
          console.log(error)
          _this.$q.notify({
            type: 'negative',
            message: 'Internal error.'
          })
        })
      }
    }
  }
}
</script>

<style scoped>
</style>
