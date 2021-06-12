<template>
  <q-card>
    <q-card-section class="text-center">
      <q-avatar size="100px" class="shadow-10">
        <img :src="avatar">
      </q-avatar>
    </q-card-section>

    <q-card-section class="q-pt-none text-center ">
      <div class="text-h3  text-grey-8 q-mb-lg">
        {{ name }}
      </div>
      <div class="text-subtitle1 text-grey-8">
        <p>
          Orders: <a @click="$router.push('/order')"> <q-badge :label="this.$store.state.order_count"></q-badge> in total </a>.
        </p>
        <p>
          Shopping cart: <a @click="$router.push('/cart')"> <q-badge :label="this.$store.state.cart_count"></q-badge> items. </a>
        </p>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "CardProfile",
  props: ['avatar', 'name']
}
</script>

<style scoped>

</style>
