import axios from 'axios';

const addBucketlistItem = {
  template: '#bucketlistItems',
  data() {
    return {
      name: undefined,
      done: undefined,
      formFilled: true,
      responseMessage: 'You cannot have a nameless item.'
    };
  },
  methods: {
    addBucketlistItem(id) {
      console.log(id)
      if(this.name){
        axios.post('http://localhost:5000/bucketlists/'+ id +'/items', {
          name: this.name,
          done: this.done,
        })
      .then((response) => {
        this.formFilled = true;
        this.responseMessage = response.data.message;
        this.$router.push({
          name: 'home'
        })
      })
    }
    }
  }
};

export default addBucketlistItem;
