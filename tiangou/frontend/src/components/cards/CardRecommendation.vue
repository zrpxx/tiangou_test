<template>
  <q-card>
    <q-img :src="img" width="100%"/>

    <q-card-section class="q-pt-none q-mt-xl" style="width: 400px">
      <div class="text-h4">
        猜你喜欢:
      </div>
      <div class="text-h5 text-grey">
        {{ name }}
      </div>
      <div class="text-subtitle1 text-grey">
        {{ desc }}
      </div>
    </q-card-section>

    <q-separator/>

    <q-card-actions>
      <q-btn flat color="primary" @click="onCheck()">
        Check it out
      </q-btn>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  name: "CardRecommendation",
  props: ['id', 'name', 'desc', 'img'],
  methods: {
    onCheck() {
      this.$router.push({name: 'detail', params:{'product_id': this.id}})
    }
  }
}
</script>

<style scoped>

</style>
