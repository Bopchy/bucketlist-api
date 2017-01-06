import axios from 'axios';

const deleteBucketlistItem = {
  template: '#deleteBucketlistItem',
  data() {
    return {
      responseMessage: undefined,
    };
  },
  created() {
    const id = this.$route.params.bucketlistId
    const itemid = this.$route.params.itemId
    axios.delete('http://localhost:5000/bucketlists/' + id + '/items/' + itemid)
      .then((response) => {
        this.responseMessage = response.data.message;
        this.$router.push({
          name: 'home'
        })
      })
  },
};

export default deleteBucketlistItem;
