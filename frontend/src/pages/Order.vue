<template>
  <div>
    <q-card class="q-mx-auto q-my-lg" style="width: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Orders</p>
      </q-card-section>
      <q-card-section>
        <q-table
          :data="orders"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
        >
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn dense round flat color="primary" @click="onClickInfo(props)" icon="info"></q-btn>
              <q-btn v-if="props.row.status === 'Created'" dense round flat color="primary" @click="onClickPay(props)" icon="payments"></q-btn>
              <q-btn v-if="props.row.status === 'Shipped'" dense round flat color="primary" @click="onClickConfirm(props)" icon="check"></q-btn>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog v-model="info" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="payments" color="primary" text-color="white" />
          <span class="q-ml-sm text-h6">Order info:</span>
        </q-card-section>
        <p class="q-ml-sm text-subtitle1 text-center" v-for="(item, index) in order_info" :key="index">{{ item.name }} * {{ item.num }}</p>
        <q-card-actions align="right">
          <q-btn flat label="OK" color="Primary" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="pay" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="payments" color="primary" text-color="white" />
          <span class="q-ml-sm">Are you sure to pay this order?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="red" v-close-popup/>
          <q-btn flat label="Yes" color="primary" v-close-popup @click="onPay()" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="confirm" class="bg-white" persistent style="width: 400px;">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="check" color="primary" text-color="white" />
          <span class="q-ml-sm">Are you sure to confirm this order?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="red" v-close-popup/>
          <q-btn flat label="Yes" color="primary" v-close-popup @click="onConfirm()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: "Order",
  data () {
    return {
      orders: [],
      loading: false,
      pay: false,
      confirm: false,
      confirmID: -1,
      payID: -1,
      info:false,
      order_info: {},
      columns: [
        {
          name: 'ID',
          required: true,
          label: 'Order ID',
          align: 'left',
          field: row => row.id,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'Order code',
          required: true,
          label: 'Order code',
          align: 'left',
          field: row => row.code,
        },
        {
          name: 'Address',
          required: true,
          label: 'Address',
          align: 'left',
          field: row => row.address,
        },
        {
          name: 'Receiver',
          required: true,
          label: 'Receiver',
          align: 'left',
          field: row => row.receiver,
        },
        {
          name: 'Mobile phone',
          required: true,
          label: 'Mobile phone',
          align: 'left',
          field: row => row.mobile,
        },
        {
          name: 'User message',
          required: true,
          label: 'Message',
          align: 'left',
          field: row => row.userMessage,
        },
        {
          name: 'Create date',
          required: false,
          label: 'Create date',
          align: 'left',
          field: row => row.createDate,
        },
        {
          name: 'Pay date',
          required: false,
          label: 'Pay date',
          align: 'left',
          field: row => row.payDate,
        },
        {
          name: 'Ship date',
          required: false,
          label: 'Ship date',
          align: 'left',
          field: row => row.shipDate,
        },
        {
          name: 'Confirm date',
          required: false,
          label: 'Confirm date',
          align: 'left',
          field: row => row.confirmDate,
        },
        {
          name: 'Status',
          required: true,
          label: 'Status',
          align: 'left',
          field: row => row.status,
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
    this.$axios.get('http://127.0.0.1:8000/api/order/get/' + this.$store.state.userid).then(function (response) {
      let res = response.data
      console.log(res)
      _this.orders = res.orders
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    onPay() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/order/pay', {
        order_id: this.payID
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully payed.'
          })
          _this.pay = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Mark error.' + res.message
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
    onClickPay(props) {
      this.payID = props.row.id
      this.pay = true
    },
    onConfirm() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/order/confirm', {
        confirm_id: this.confirmID
      }).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Successfully confirmed.'
          })
          _this.pay = false
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Mark error.' + res.message
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
    onClickConfirm(props) {
      this.confirmID = props.row.id
      this.confirm = true
    },
    onClickInfo(props) {
      let _this = this
      this.$axios.get('http://127.0.0.1:8000/api/order/' + props.row.id).then(function (response) {
        console.log(response)
        let res = response.data
        if(res.status === 'Success') {
          _this.order_info = res.item
          _this.info = true
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Mark error.' + res.message
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
</script>

<style scoped>
</style>
