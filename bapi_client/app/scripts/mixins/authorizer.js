// More about mixins here: http://vuejs.org/v2/guide/mixins.html
const authorizer = {
  // => is short way of declaring a function that acts as a container
  // it does not interfere with the scoping of this object (esp when using 'this'/self)
  beforeCreate() {
    const bapiToken = window.localStorage.getItem('bapiToken');
    if (bapiToken) {
      this.bapiToken = JSON.parse(bapiToken); // {"token": 'askdkajaksdjskd'}
      return;
    }

    console.log('Not logged in. Taking them to sign in page');

    // See this: http://router.vuejs.org/en/api/route-object.html
    if (this.$route.name !== 'sign-in') {
      this.$router.push({ name: 'sign-in' });
    }
  },
};

export default authorizer;

// Other ways to achieve the same
// http://router.vuejs.org/en/advanced/navigation-guards.html
