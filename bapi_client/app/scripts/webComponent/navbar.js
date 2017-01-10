const navbarComponent = {
  template: '#myNavbar',
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
