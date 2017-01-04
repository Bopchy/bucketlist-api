import axios from 'axios';

const signIn = {
  template: '#signin',
  data() {
    return {
      username: undefined,
      password: undefined,
      formFilled: false,
      responseMessage: 'Please ensure you fill all the input.',
    };
  },
  methods: {
    loginUser() {
      if (this.username && this.password) {
        axios.post('http://localhost:5000/auth/login', {
          username: this.username,
          password: this.password,
        })
          .then((response) => {
            this.formFilled = true;
            this.responseMessage = response.data.message;
            // Browser localStorage API stores data as a string in the browser -- data
            // doesn't expire till you remove it.
            // JSON.stringify is an API that stringifies objects
            // Anything attached window (a built-in browser provided global variable)
            // see links
            // https://developer.mozilla.org/en/docs/Web/API/Window
            // https://developer.mozilla.org/en/docs/Web/API/Document
            // https://developer.mozilla.org/en/docs/Web/API/Navigator
            window.localStorage.setItem('bapiToken', JSON.stringify(response.data));
            this.$router.push({
              name: 'home',
            });
          });
      } else {
        console.log(this.responseMessage);
      }
    },
  },
};

export default signIn;
