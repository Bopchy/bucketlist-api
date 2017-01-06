import axios from 'axios';

const editBucketlist = {
  template: '#editBucketlist',
  data() {
    return {
      name: undefined,
      responseMessage: "Go ahead and change your bucketlist's name ",
    };
  },
  methods: {
    editBucketlist(input) {
      const id = this.$route.params.bucketlistId
      if (this.name) {
        axios.put('http://localhost:5000/bucketlists/' + id, {
            name: this.name
          })
          .then((response) => {
            this.responseMessage = response.data.message;
            this.name = undefined;
            this.$router.push({
              name: 'home'
            })
          }).catch((err) => {
            console.error(err);
          })
      }
    }
  },
};

export default editBucketlist;
