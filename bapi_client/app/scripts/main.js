// Imports required components
import home from './components/home';
import signUp from './components/signUp';
import signIn from './components/signIn';
import addBucketlist from './components/addBucketlist';
import addBucketlistItem from './components/addBucketlistItem';
import editBucketlist from './components/editBucketlist';
import editBucketlistItem from './components/editBucketlistItem';
import deleteBucketlist from './components/deleteBucketlist';
import deleteBucketlistItem from './components/deleteBucketlistItem';

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
  path: '/bucketlist/:bucketlistId/add-item',
  name: 'addBucketlistItem',
  component: addBucketlistItem,
}, {
  path: '/bucketlists/:bucketlistId',
  name: 'editBucketlist',
  component: editBucketlist,
}, {
  path: '/bucketlists/:bucketlistId/edit-item/:itemid',
  name: 'editBucketlistItem',
  component: editBucketlistItem,
}, {
  path: '/bucketlists/:bucketlistId',
  name: 'deleteBucketlist',
  component: deleteBucketlist,
}, {
  path: '/bucketlists/:bucketlistId/items/:itemId',
  name: 'deleteBucketlistItem',
  component: deleteBucketlistItem,
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
