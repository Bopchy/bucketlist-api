import axios from 'axios';

// More about mixins here: http://vuejs.org/v2/guide/mixins.html
const authorizer = {
    // => is short way of declaring a function that acts as a container
    // it does not interfere with the scoping of this object (esp when using 'this'/self)
  beforeCreate() {
    const bapiToken = window.localStorage.getItem('bapiToken');
    if (bapiToken) {
      this.bapiToken = JSON.parse(bapiToken); // {"token": 'askdkajaksdjskd'}
      axios.interceptors.request.use((config) => {
        config.headers.common['Authorization'] = 'Token ' + this.bapiToken.token;
        return config;
      });
      return;
    } else if (this.$route.name === 'signUp') {
      return;
    } else if (this.$route.name === 'signIn') {
      return;
    }
      // See this: http://router.vuejs.org/en/api/route-object.html
      // Other ways to achieve the same
      // http://router.vuejs.org/en/advanced/navigation-guards.html
    console.log('Not logged in. Taking them to sign in page');
    this.$router.push({
      name: 'signIn',
    });
  },
};

export default authorizer;
