import Detail from "pages/Detail";

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Login')},
      { path: 'reg', component: () => import('pages/Register')},
      { path: 'index', component: () => import('pages/Index.vue') },
      { path: 'store', component: () => import('pages/Product') },
      { path: 'order', component: () => import('pages/Order')},
      { path: 'cart', component: () => import('pages/ShoppingCart')},
      { path: 'product', name:'detail', component: () => import('pages/Detail')},
      { path: 'admin/category', component: () => import('pages/CategoryAdmin') },
      { path: 'admin/property', component: () => import('pages/PropertyAdmin') },
      { path: 'admin/product', component: () => import('pages/ProductAdmin') },
      { path: 'admin/order', component: () => import('pages/OrderAdmin')}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
