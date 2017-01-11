const navbarComponent = {
  template: '#myNavbar',
  data() {
    return {
      currentRoute: undefined,
      isLoggedIn: window.localStorage.getItem('bapiToken') ? true: false, //ternary expression
    };
  },
  mounted() {
    this.currentRoute = this.$route.name;
    console.log('Your current route', this.$route);
  },
  methods: {
    signOut() {
      console.log(this.$route)
      console.log('The navbar sign out button was clicked')
      const loggedIn = window.localStorage.getItem('bapiToken');
      if (loggedIn) {
        this.responseMessage = "See you later!";
        window.localStorage.clear();
        this.$router.push({
          name: 'signIn'
        })
      }
    },
    signUp() {
      console.log('Directing to sign up.')
      this.$router.push({
        name: 'signUp'
      })
    },
    signIn() {
      console.log('Directing to sign in.')
      this.$router.push({
        name: 'signIn'
      })
    },
  }
};

export default navbarComponent;
