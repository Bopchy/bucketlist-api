import axios from 'axios';

const addBucketlist = {
  template: '#bucketlists',
  data() {
    return {
      name: undefined,
      formFilled: true,
      responseMessage: 'Name your new bucketlist',
    };
  },
  methods: {
    addBucketlist(input) {
      console.log(input)
      if (this.name) {
        axios.post('http://localhost:5000/bucketlists/', {
          name: this.name
        })
        .then((response) => {
          this.formFilled = true;
          this.responseMessage = response.data.message;
          this.name = undefined;
          this.$router.push({
            name: 'home',
          })
        })
      }
    },
  }
};

export default addBucketlist;

// Send a POST request
// axios({
//   method: 'post',
//   url: '/user/12345',
//   data: {
//     firstName: 'Fred',
//     lastName: 'Flintstone'
//   }
// });
