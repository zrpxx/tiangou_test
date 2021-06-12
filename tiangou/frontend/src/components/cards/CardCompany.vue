<template>
  <q-card class="text-white" :style="{'background-image': background_image}">
    <q-card-section>
      <div class="text-h3 text-center">
        {{ food_name }}
      </div>
    </q-card-section>
    <q-separator/>
    <q-card-section>
      <div class="text-h3 text-weight-bolder text-center">
        <q-icon name="restaurant_menu"></q-icon>
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <div class="text-h4 text-weight-bolder text-center">
        Rank: {{ food_score }}
      </div>
    </q-card-section>
    <q-card-section>
      <div class="text-h6 text-weight-bolder text-center">
        Brand: {{ food_brand }}
      </div>
    </q-card-section>
    <q-card-actions vertical align="center">
      <q-btn class="text-capitalize q-mb-md" color="primary" @click="onDetail()">More info</q-btn>
    </q-card-actions>
    <q-separator/>
    <q-card-section class="text-center" v-if="food_category.length > 0">
      <q-badge  class="q-mx-md q-my-sm" v-for="category in food_category" v-bind:key="category.key" color="primary">{{ category }}</q-badge>
    </q-card-section>

  </q-card>
</template>

<script>
export default {
  name: "CardCompany",
  props:['background_image', 'food_name', 'food_id', 'food_brand', 'food_score', 'food_category'],
  methods: {
    onDetail() {
      this.$router.push({
        name: 'detail',
        params: {
          food_id: this.food_id
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
