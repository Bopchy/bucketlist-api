const landingPage = {
  template: '#landingPage',
  methods: {
    toHome() {
      console.log('Directing to home')
      this.$router.push({
        name: 'home',
      })
    },
  },
};

export default landingPage;
