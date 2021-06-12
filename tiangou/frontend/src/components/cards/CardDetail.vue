<template>
  <div>
    <q-card class="text-white" :style="{'background-image': background_image}">
      <q-card-section>
        <br>
        <div class="text-h1 text-weight-bolder text-center">
          {{ product.name }}
        </div>
        <br>
      </q-card-section>
      <q-separator/>
      <q-card-section>
        <q-img :src="thumbnail" width="100%"></q-img>
      </q-card-section>
      <q-card-section class="q-pa-none">
        <div class="text-h2 text-weight-bolder text-center">
          Category: {{ product.category_name }}
        </div>
      </q-card-section>
      <br>
      <q-card-section>
        <div class="text-h2 text-weight-bolder text-center">
          Description
          <br>
          <div class="text-h2 text-center">
            {{ product.subtitle }}
          </div>
        </div>
      </q-card-section>
      <br>
      <q-card-section>
        <div class="text-h2 text-weight-bolder text-center">
            Property
        </div>
      </q-card-section>
      <q-card-section>
        <div class="text-h3 text-center q-mb-md" v-for="(property, index) in properties" :key="index">
          {{ property.property }} : {{ property.value }}
        </div>
      </q-card-section>
      <q-card-section>
        <div class="text-h2 text-weight-bolder text-center">
          Stock
          <br>
          <div class="text-h2 text-center">
            {{ product.stock }}
          </div>
        </div>
      </q-card-section>
      <br>
      <q-card-section>
        <q-img :src="detail" width="100%"></q-img>
      </q-card-section>
      <q-separator/>
      <q-card-section class="text-center">
        <div class="text-h3 text-center q-mb-md">
          Buy now
        </div>
        <q-btn label="Add to cart" color="primary" class="q-mx-xl" @click="onAddCart()"></q-btn>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
export default {
  name: "CardDetail",
  props:['background_image', 'product', 'thumbnail', 'detail', 'properties'],
  data() {
    return {

    }
  },
  created() {

  },
  methods: {
    onAddCart() {
      let _this = this
      this.$axios.post('http://127.0.0.1:8000/api/cart/create', {
          uid: this.$store.state.userid,
          pid: this.product.id
      }).then(function (response) {
        let res = response.data
        if(res.status === 'Success') {
          _this.$q.notify({
            type: 'positive',
            message: 'Product added to cart'
          })
        } else {
          if(res.message === 'Unauthorized')
            _this.$router.push('/')
          _this.$q.notify({
            type: 'negative',
            message: 'Add failed. ' + res.message
          })
        }
      }).catch(function (error) {
        console.log(error);
        _this.$q.notify({
          type: 'negative',
          position: 'top',
          message: 'Internal error.'
        })
      })
    }
  }
}
</script>

<style scoped>

</style>
