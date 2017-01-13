import axios from 'axios';

const home = {
  template: '#home',
  data() {
    return {
      message: 'Your bucketlists',
      buckets: []
    };
  },
  // other Vue component events: created, beforeMount, mounted, beforeUpdate, updated
  beforeCreate() {
    // Do anything here eg. fetch new data, verify some things etc
    axios.get('http://localhost:5000/bucketlists/')
      .then((response) => {
        console.log(response);
        // Data structures come with built in functions
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array
        this.buckets = response.data.bucketlists.map((bucket) => {
          // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String
          bucket.date_created = bucket.date_created.replace('-0000', '');
          return bucket;
        });
      }).catch((err) => {
        console.error(err);
      })
  },
};

export default home;
