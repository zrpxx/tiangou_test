<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <div class="text-center q-pt-lg">
              <div class="col text-h4 ellipsis">
                Log in
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <q-form
              class="q-gutter-md"
            >
              <q-input
                filled
                v-model="username"
                label="Username"
                lazy-rules
              />

              <q-input
                type="password"
                filled
                v-model="password"
                label="Password"
                lazy-rules

              />

              <div class="q-ml-lg q-mt-lg text-center">
                <q-btn label="Login" @click="onLogin()" type="button" color="primary"/>
                <q-btn label="Register" @click="goReg()" type="button" color="white" text-color="primary"/>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { Notify } from 'quasar'
export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  created() {
    sessionStorage.setItem('token', '')
  },
  methods: {
    onLogin() {
      let _this = this
      this.$axios.post('http://tiangou.zrp.cool/api/login', {
        username: this.username,
        password: this.password
      }).then(function (response) {
        let res = response.data
        if(res.status === 'Success') {
          _this.$store.commit('login', {
            id: res.user_id,
            name: _this.username,
            isAdmin: res.user_isAdmin,
            order_count: res.order_count,
            cart_count: res.shopping_cart_count,
            token: res.token
          })
          _this.$router.replace('/index')
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Login failed. ' + res.message
          })
        }
      }).catch(function (error) {
        console.log(error);
        _this.$q.notify({
          type: 'negative',
          position: 'top',
          message: 'Internal error.'
        })
      });
    },
    goReg() {
      this.$router.push('/reg')
    }
  }
}
</script>

<style>
.bg-image {
  background-image: linear-gradient(45deg, #258bc7 0%, #e587b4 100%);
}
</style>
