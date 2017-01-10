import axios from 'axios';

const signUp = {
  template: '#sign-up',
  data() {
    return {
      message: 'Please Sign Up',
      email: undefined,
      username: undefined,
      password: undefined,
      formFilled: false,
      responseMessage: 'Please ensure you fill all the input.',
    };
  },
  methods: {
    registerUser() {
      if (this.email && this.username && this.password) {
        // everything is defined
        axios.post('http://localhost:5000/auth/register', {
          email: this.email,
          username: this.username,
          password: this.password,
        })
          .then((response) => {
            this.formFilled = true;
            this.responseMessage = response.data.message;
            this.email = this.username = this.password = undefined;
            setTimeout(() => {
              this.$router.push({
                name: 'signIn',
              });
            }, 2000);
          })
          .catch((error) => {
            console.log(error);
            this.responseMessage = error.response.data.message;
          });
      } else {
        this.formFilled = false;
      }
    },
  },
};

export default signUp;
