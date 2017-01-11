const signOut = {
  template: '#signOut',
  data() {
    return {
      responseMessage: undefined,
      currentRoute: undefined,
    };
  },
  created() {
    const loggedIn = window.localStorage.getItem('bapiToken');
    if (loggedIn) {
      this.responseMessage = "See you later!";
      window.localStorage.clear();
    } else {
      this.responseMessage = "You are not signed in at the moment.";
      this.$route.push({
        name: 'signIn'
      })
    }
  },
};

export default signOut;
