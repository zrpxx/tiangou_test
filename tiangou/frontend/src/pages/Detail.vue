<template>
  <q-page class="q-pa-sm q-mx-xl q-mt-lg">
    <card-detail :background_image="getBackground()" :product="product" :thumbnail="product_img.thumbnail" :properties="property" :detail="product_img.detail"></card-detail>
  </q-page>
</template>

<script>
import CardDetail from "components/cards/CardDetail";
export default {
  name: "Detail",
  components: {CardDetail},
  data () {
    return {
      loggedIn: false,
      product_id: -1,
      product: {},
      product_img: {},
      property: {},
      background_img: [
        'linear-gradient(to top, #30cfd0 0%, #330867 100%)',
        'linear-gradient(87deg, rgb(45, 206, 137), rgb(45, 206, 204)) !important',
        'linear-gradient(137deg, rgb(250, 128, 114), rgb(148, 0, 213)) !important'
      ]
    }
  },
  created() {
    if(this.$route.params.product_id !== undefined)
      this.product_id = this.$route.params.product_id
    let _this = this
    this.$axios.get('https://tiangou.zrp.cool/api/product/' + this.product_id).then(function (response) {
      let res = response.data
      if(res.status === 'Success') {
        _this.product = res.product
        _this.product.category_name = res.category_name
        _this.product_img.thumbnail = res.thumbnail_pic
        _this.product_img.detail = res.detail_pic
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
    this.$axios.get('https://tiangou.zrp.cool/api/product_property/' + this.product_id).then(function (response) {
      let res = response.data
      if(res.status === 'Success') {
        _this.property = res.property
        console.log(_this.property)
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
  },
  methods: {
    getBackground() {
      return this.background_img[Math.floor(Math.random() * 3)]
    }
  }
}
</script>

<style scoped>
</style>
