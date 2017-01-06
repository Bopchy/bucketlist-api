import axios from 'axios';

const home = {
  template: '#home',
  data() {
    return {
      message: 'You are at home now',
      buckets: []
    };
  },
  // other Vue component events: created, beforeMount, mounted, beforeUpdate, updated
  beforeCreate() {
    // Do anything here eg. fetch new data, verify some things etc
    axios.get('http://localhost:5000/bucketlists/')
      .then((response) => {
        console.log(response);
        this.buckets = response.data.bucketlists;
      }).catch((err) => {
        console.error(err);
      })
  },
};

export default home;
