<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          天狗商城 <q-badge v-if="$store.state.isAdmin" class="text-subtitle1" color="red" label="Admin"></q-badge>
        </q-toolbar-title>

        <div class="text-subtitle1"> Made with ❤ by 张濡芃，李纯洋，周延晨 & 周光彪</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item v-ripple exact to="/" v-if="!$store.state.loggedIn && $route.path === '/'">
          <q-item-section avatar>
            <q-icon name="login"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Login</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-ripple exact to="/reg" v-if="!$store.state.loggedIn && $route.path === '/reg'">
          <q-item-section avatar>
            <q-icon name="person_add"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Register</q-item-label>
          </q-item-section>
        </q-item>


        <q-item v-ripple exact to="/index" v-if="$store.state.loggedIn">
          <q-item-section avatar>
            <q-icon name="dashboard"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-ripple exact to="/store">
          <q-item-section avatar>
            <q-icon name="category"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Products</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-ripple exact to="/cart" v-if="$store.state.loggedIn">
          <q-item-section avatar>
            <q-icon name="shopping_cart"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Shopping cart</q-item-label>
          </q-item-section>
        </q-item>

        <q-item v-ripple exact to="/order" v-if="$store.state.loggedIn">
          <q-item-section avatar>
            <q-icon name="list"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Orders</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item
          switch-toggle-side
          expand-separator
          icon="settings"
          label="Administration"
          v-if="$store.state.isAdmin"
        >
          <q-item v-ripple exact to="/admin/category">
            <q-item-section avatar>
              <q-icon name="settings"/>
            </q-item-section>
            <q-item-section>
              <q-item-label>Manage categories</q-item-label>
            </q-item-section>
          </q-item>

          <q-item v-ripple exact to="/admin/property">
            <q-item-section avatar>
              <q-icon name="settings"/>
            </q-item-section>
            <q-item-section>
              <q-item-label>Manage properties</q-item-label>
            </q-item-section>
          </q-item>

          <q-item v-ripple exact to="/admin/product">
            <q-item-section avatar>
              <q-icon name="settings"/>
            </q-item-section>
            <q-item-section>
              <q-item-label>Manage products</q-item-label>
            </q-item-section>
          </q-item>

          <q-item v-ripple exact to="/admin/order">
            <q-item-section avatar>
              <q-icon name="settings"/>
            </q-item-section>
            <q-item-section>
              <q-item-label>Manage orders</q-item-label>
            </q-item-section>
          </q-item>

        </q-expansion-item>

        <q-item v-ripple clickable @click="onLogout()" v-if="$store.state.loggedIn">
          <q-item-section avatar>
            <q-icon name="logout"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Log out</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>

export default {
  name: 'MainLayout',
  data () {
    return {
      leftDrawerOpen: false
    }
  },
  created() {
    //在页面加载时读取sessionStorage里的状态信息
    if (sessionStorage.getItem('store')) {
      this.$store.replaceState(Object.assign({}, this.$store.state, JSON.parse(sessionStorage.getItem('store'))));
    }

    //在页面刷新时将vuex里的信息保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(this.$store.state));
    });
  },
  methods: {
    onLogout() {
      this.$store.commit('logout')
      this.$router.push('/')
    }
  }
}
</script>
