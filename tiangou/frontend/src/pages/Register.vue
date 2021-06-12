<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <div class="text-center q-pt-lg">
              <div class="col text-h4 ellipsis">
                Register
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
                :rules="[ val => val && val.length > 0 || 'Please type a username']"
              />

              <q-input
                type="password"
                filled
                v-model="password"
                label="Password"
                lazy-rules
                :rules="[val => val !== null && val !== '' || 'Please type a password']"
              />

              <div class="q-ml-lg q-mt-lg text-center">
                <q-btn label="Register" @click="onReg()" type="button" color="primary"/>
                <q-btn label="Login" @click="goLogin()" type="button" color="white" text-color="primary"/>
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
      password: '',
      loggedIn: false
    }
  },
  methods: {
    onReg() {
      if(this.username === '' || this.password === '')
        return
      let _this = this
      this.$axios.post('http://tiangou.zrp.cool/api/register', {
        username: this.username,
        password: this.password
      }).then(function (response) {
        let res = response.data
        if(res.status === 'Success') {
          _this.$router.replace('/')
        } else {
          _this.$q.notify({
            type: 'negative',
            message: 'Register failed. ' + res.message
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
    goLogin() {
      this.$router.push('/')
    }
  }
}
</script>

<style>
.bg-image {
  background-image: linear-gradient(45deg, #258bc7 0%, #e587b4 100%);
}
</style>
