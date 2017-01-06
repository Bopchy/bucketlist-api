import axios from 'axios';

const deleteBucketlist = {
  template: '#deleteBucketlist',
  data() {
    return {
      showModal: false,
      responseMessage: undefined,
    };
  },

  created() {
    // showModal = true;
    const id = this.$route.params.bucketlistId
    axios.delete('http://localhost:5000/bucketlists/' + id)
      .then((response) => {
        this.responseMessage = response.data.message;
        this.$route.push({
          name: 'home'
        })
      })
  }

};

export default deleteBucketlist;


// register modal component
// Vue.component('modal', {
//   template: '#modal-template'
// })
//
// // start app
// new Vue({
//   el: '#app',
//   data: {
//     showModal: false
//   }
// })
