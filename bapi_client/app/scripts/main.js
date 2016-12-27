// Imports required components
import home from './components/home';
import signUp from './components/signUp';
import signIn from './components/signIn';
import addBucketlist from './components/addBucketlist';

import authorizer from './mixins/authorizer';

// Equivalent of 'DEBUG = True' in Flask
Vue.config.debug = true;

// Define all the application routes
const appRoutes = [{
  path: '/',
  name: 'home',
  component: home,
}, {
  path: '/sign-up',
  name: 'signUp',
  component: signUp,
}, {
  path: '/sign-in',
  name: 'signIn',
  component: signIn,
}, {
  path: '/bucketlist/create',
  name: 'addBucketlist',
  component: addBucketlist,
}, {
  // Directs to home if path is invalid
  path: '/*',
  redirect: '/',
}];

// Lets you call the mixin authorizer only once
Vue.mixin(authorizer);

const app = new Vue({
  router: new VueRouter({ routes: appRoutes }),
});
// attaches const app to #app element
app.$mount('#app');
