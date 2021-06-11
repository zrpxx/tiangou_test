<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Shopping cart</p>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="cartItems"
          :columns="columns"
          :pagination.sync="pagination"
          :row-key="row => row.product_name"
          :loading="loading"
          selection="multiple"
          :selected.sync="selected"
        >
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td auto-width>
                <q-checkbox class="q-mx-auto" dense v-model="props.selected"/>
              </q-td>
              <q-td key="Name">
                {{ props.row.product_name }}
              </q-td>
              <q-td key="Price">
                {{ props.row.product_name }}
              </q-td>
              <q-td key="Number" :props="props">
                {{ props.row.number }}
                <q-popup-edit v-model="props.row.number" title="Update number of product" buttons persistent
                :validate="validateNumber" @hide="validateNumber">
                  <q-input type="number" v-model="props.row.number" dense autofocus
                           lazy-rules
                           :rules="[ val => val && val.length > 0 || 'Please type a number',
                      val => val && val > 0 && val % 1 === 0 || 'Please type a valid number'
                      ]"/>
                </q-popup-edit>
              </q-td>
              <q-td key="Total price">
                ￥{{ props.row.product_price * props.row.number }}
              </q-td>
              <q-td key="Actions" auto-width>
                  <q-btn class="q-mx-lg"  color="negative" @click="onDelete(props)" icon="delete" />
              </q-td>
            </q-tr>
          </template>
          <template v-slot:bottom>
            <q-btn class="float-right" color="primary" label="Check out" @click="onCheckout()"></q-btn>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog v-model="checkoutDialog1" class="bg-white" persistent style="width: 400px;">
      <q-card class="q-pa-xl">
        <q-form
          @submit="onSubmitInfo"
          style="width: 400px"
        >
          <q-input
            filled
            v-model="name"
            label="Receiver name *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a receiver name']"
          />

          <q-input
            filled
            v-model="mobile"
            type="number"
            label="Receiver phone *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a receiver phone']"
          />

          <q-input
            filled
            v-model="address"
            label="Receiver address *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a receiver address']"
          />

          <q-input
            filled
            v-model="post"
            label="Receiver postcode *"
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Please type a receiver postcode']"
          />

          <q-input
            filled
            v-model="message"
            label="Receiver message"
          />

          <div class="q-mt-lg">
            <q-btn label="Submit" type="submit" color="primary"/>
            <q-btn label="Cancel" color="primary" flat class="q-ml-sm" v-close-popup />
          </div>
        </q-form>
      </q-card>
    </q-dialog>

    <q-dialog v-model="checkoutDialog2" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="payments" color="primary" text-color="white" />
          <span class="q-ml-sm">Do you want to pay the order or just generate it?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Just generate it" v-close-popup @click="onGenerate()"/>
          <q-btn flat label="Pay it" color="primary" v-close-popup @click="onPay()" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="confirmDialog" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="list_alt" color="primary" text-color="white" />
          <span class="q-ml-sm">Order generated successfully!</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Check it out" color="primary" v-close-popup @click="$router.push('/order')" />
        </q-card-actions>
      </q-card>
    </q-dialog>


    <q-dialog v-model="deleteDialog" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="primary" text-color="white" />
          <span class="q-ml-sm">Are you sure to delete this product from shopping cart?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup/>
          <q-btn flat label="Delete anyway" color="red" v-close-popup @click="onConfirmDelete()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>

export default {
  name: "Shoppingcart",
  data () {
    return {
      cartItems: [],
      loading: false,
      selected: [],
      deleteID: -1,
      checkoutDialog1: false,
      checkoutDialog2: false,
      confirmDialog: false,
      totalPay: -1,
      name: '',
      mobile: '',
      address: '',
      message: '',
      post: '',
      deleteDialog: false,
      generateID: -1,
      columns: [
        {
          name: 'Name',
          required: true,
          label: 'Product name',
          align: 'left',
          field: row => row.product_name,
        },
        {
          name: 'Price',
          required: true,
          label: 'Product price',
          align: 'left',
          field: row => row.product_price,
          format: val => `¥${val}`,
        },
        {
          name: 'Number',
          required: true,
          label: 'Number of product',
          align: 'left',
          field: row => row.number
        },
        {
          name: 'Total price',
          required: true,
          label: 'Total price',
          align: 'left',
          field: row => (row.number * row.product_price)
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
    this.$axios.post('http://127.0.0.1:8000/api/cart/products',{
      uid: this.$store.state.userid
    }).then(function (response) {
      let res = response.data
      console.log(res)
      _this.cartItems = res.cart_products
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    validateNumber(val) {
      return val && val > 0 && val % 1 === 0;
    },
    onDelete(props) {
      for(let i = 0; i < this.cartItems.length; i++) {
        if(props.row.product_name === this.cartItems[i].product_name) {
          this.deleteID = this.cartItems[i].pid
          break
        }
      }
      console.log(this.deleteID)
      this.deleteDialog = true
    },
    onConfirmDelete() {
      let _this = this
      this.$axios.delete('http://127.0.0.1:8000/api/cart/delete', {
        data: {
          uid: this.$store.state.userid,
          pid: this.deleteID
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
    onCheckout() {
      if(this.selected.length <= 0) {
        this.$q.notify({
          type: 'warning',
          message: 'Please select items to check out'
        })
        return
      }
      this.totalPay = 0
      for(let i = 0; i < this.selected.length; i++) {
        this.totalPay += this.selected[i].number * this.selected[i].product_price
      }
      this.checkoutDialog1 = true
    },
    onGenerate() {
      let pids = []
      let nums = []
      for(let i = 0; i < this.selected.length; i++) {
        for(let j = 0; j < this.cartItems.length; j++) {
          if(this.selected[i].product_name === this.cartItems[j].product_name) {
            pids.push(this.cartItems[j].pid)
            nums.push(this.selected[i].number)
            break
          }
        }
      }
      console.log(pids)
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/order/create', {
        userid: this.$store.state.userid,
        items: pids,
        nums: nums,
        orderInfo: {
          name: this.name,
          mobile: this.mobile,
          address: this.address,
          message: this.message,
          post: this.post
        }
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.checkoutDialog2 = false
          _this.confirmDialog = true
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Order create error.' + res.message
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
    onPay() {
      let pids = []
      let nums = []
      for(let i = 0; i < this.selected.length; i++) {
        for(let j = 0; j < this.cartItems.length; j++) {
          if(this.selected[i].product_name === this.cartItems[j].product_name) {
            pids.push(this.cartItems[j].pid)
            nums.push(this.selected[i].number)
            break
          }
        }
      }
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/order/create', {
        userid: this.$store.state.userid,
        items: pids,
        nums: nums,
        orderInfo: {
          name: this.name,
          mobile: this.mobile,
          address: this.address,
          message: this.message,
          post: this.post
        }
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.generateID = res.order_id
          _this.$axios.post('http://127.0.0.1:8000/api/order/pay', {
            order_id: _this.generateID
          }).then(function (response) {
            console.log(response)
            let res = response.data
            if(res.status === 'Success') {
              _this.checkoutDialog2 = false
              _this.confirmDialog = true
            } else {
              _this.$q.notify({
                type: 'negative',
                message: 'Order pay error.' + res.message
              })
            }
          }).catch(function (error) {
            console.log(error)
            _this.$q.notify({
              type: 'negative',
              message: 'Internal error.'
            })
          })
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Order create error.' + res.message
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
    onSubmitInfo() {
      this.checkoutDialog1 = false
      this.checkoutDialog2 = true
    }
  }
}
</script>

<style scoped>
</style>
