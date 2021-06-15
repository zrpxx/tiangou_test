<template>
  <div>
    <q-card class="q-mx-auto q-mt-xl" style="width: 80%; height: 80%">
      <q-card-section>
        <p class="text-h2 q-mt-lg">Products</p>
      </q-card-section>
      <q-card-section>
        <q-table
          grid
          :data="products"
          :columns="columns"
          :pagination.sync="pagination"
          row-key="id"
          :loading="loading"
          hide-header
          :filter="filter"
          :filter-method="filterMethod"
        >
          <template v-slot:top-left>
            <q-select
              v-model="filter.visibleCategories"
              multiple
              outlined
              rounded
              options-dense
              emit-value
              map-options
              :options="categories"
              label="Categories"
              style="width: 250px"
            />
          </template>
          <template v-slot:top-right>

            <q-input dense debounce="300" v-model="filter.searchStr" placeholder="Search">
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:item="props">
            <div
              class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition">
              <q-card>
                <q-img :src="props.row.thumbnail_pic" width="100%"/>
                <q-list padding separator>
                  <q-item>
                    <q-item-section>
                      <q-item-label class="text-h6"> Product name </q-item-label>
                      <q-item-label class="text-subtitle1 text-primary">{{ props.row.name }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label class="text-h6"> Product description </q-item-label>
                      <q-item-label class="text-subtitle1 text-primary">{{ props.row.subtitle }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label class="text-h6"> Stock </q-item-label>
                      <q-item-label class="text-subtitle1 text-primary">{{ props.row.stock }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label class="text-h6"> Product price </q-item-label>
                      <q-item-label class="text-subtitle1 text-primary text-weight-bold"><del class="q-mr-sm text-grey text-weight-regular">￥{{ props.row.original_price }}</del>￥{{ props.row.promote_price }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item class="text-center">
                    <q-btn label="Check it out" color="primary" @click="onCheck(props)" />
                  </q-item>
                </q-list>
              </q-card>
            </div>
          </template>

        </q-table>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
export default {
  name: "ProductList",
  data () {
    return {
      categories: [],
      categoryMap: {},
      properties: [],
      propertyMap: {},
      newProperty: {},
      products: [],
      filter: {
        searchStr: '',
        visibleCategories: []
      },
      loading: false,
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
        },
        {
          name: 'Promote price',
          required: true,
          label: 'Product promote price',
          align: 'left',
          field: row => row.promote_price,
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
        }
      ],
      pagination: {
        rowsPerPage: 25
      }
    }
  },
  created() {
    this.loading = true
    let _this = this
    this.$axios.get('https://tiangou.zrp.cool/api/categories').then(function (response) {
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
      _this.filter.visibleCategories = _this.categories
      _this.$forceUpdate()
    })
    this.$axios.get('https://tiangou.zrp.cool/api/products').then(function (response) {
      let res = response.data
      console.log(res)
      _this.products = res.products
      console.log(_this.products)
      _this.$forceUpdate()
    })
    this.loading = false
  },
  methods: {
    onCheck(props) {
      this.$router.push({
        name: 'detail',
        params: {
          product_id: props.row.id
        }
      })
    },
    filterMethod() {
      return this.products.filter(row => {
        return (this.filter.visibleCategories.indexOf(this.categoryMap.get(row.category_id)) !== -1) && (row.name.toLowerCase().indexOf(this.filter.searchStr.toLowerCase()) !== -1)
      })
    }
  }
}
</script>

<style scoped>
</style>
