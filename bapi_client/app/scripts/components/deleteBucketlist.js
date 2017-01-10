import axios from 'axios';

const deleteBucketlist = {
  template: '#deleteBucketlist',
  data() {
    return {
      responseMessage: undefined,
    };
  },

  created() {
    const id = this.$route.params.bucketlistId
    axios.delete('http://localhost:5000/bucketlists/' + id)
      .then((response) => {
        this.responseMessage = response.data.message;
        this.$router.push({
          name: 'home'
        })
      })
  }
};

export default deleteBucketlist;
