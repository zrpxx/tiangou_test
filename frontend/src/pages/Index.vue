<template>
  <q-page class="q-pa-sm flex flex-center">
      <card-profile class="q-mx-lg" style="width: 20%;" :name="'Hello, ' + $store.state.username" :avatar="'https://cdn.quasar.dev/img/boy-avatar.png'"></card-profile>
      <CardCafe class="q-mx-lg" :id="random_product_id" :name="random_product_name" :img="random_product_img" :desc="random_product_desc"></CardCafe>
  </q-page>
</template>

<script>
export default {
  name: "PageIndex",
  components: {
    CardProfile: () => import('components/cards/CardProfile'),
    CardCafe: () => import('components/cards/CardRecommendation')
  },
  data() {
    return {
      random_product_name: '...',
      random_product_id: -1,
      random_product_img: '',
      random_product_desc: ''
    }
  },
  mounted() {
    let _this = this
    this.$axios.get('http://127.0.0.1:8000/api/user/info/' + this.$store.state.userid).then(function (response) {
      let res = response.data
      if(res.status === 'Success') {
        _this.$store.commit('updateCount', {
          cart: res.shopping_cart_count,
          order: res.order_count
        })
      } else {
        _this.$q.notify({
          type: 'negative',
          message: 'Loading failed.'
        })
      }
    }).catch(function (error) {
      console.log(error)
      _this.$q.notify({
        type: 'negative',
        position: 'top',
        message: 'Internal error.'
      })
    })
    this.$axios.get('http://127.0.0.1:8000/api/random').then(function (response) {
      let res = response.data
      if(res.status === 'Success') {
        _this.random_product_id = res.product.id
        _this.random_product_name = res.product.name
        _this.random_product_desc = res.product.subtitle
        _this.random_product_img = res.product_thumbnail
      } else {
        _this.$q.notify({
          type: 'negative',
          message: 'Loading failed.'
        })
      }
    }).catch(function (error) {
      console.log(error)
      _this.$q.notify({
        type: 'negative',
        position: 'top',
        message: 'Internal error.'
      })
    })
  }
}
</script>

<style scoped>

</style>
