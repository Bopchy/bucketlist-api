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
  // The following methods sub-object are accesible in this component events, sibling methods
  // and also in the DOM/HTML/this component's template if attached to an event eg click event
  beforeRouteEnter(to, from, next) {
    // const loggedIn = window.localStorage.getItem('bapiToken');
    // if (this.loggedIn) {
    //   console.log(this.bapiToken);
    // axios.get('http://localhost:5000/bucketlists/')
    //   .then((response) => {
    //     // Accesses this next before home component (represented as thisComponent) is instantiated
    //     next((thisComponent) => {
    //       // Assigning result of response to buckets
    //       console.log(response);
    //       thisComponent.buckets = response.data.bucketlists;
    //     })
    //   }).catch((err) => {
    //     console.log(err);
    //     next()
    //   })
    // } else {
    //   this.$router.push({
    //     name: 'sign-in',
    //   });
    // }
    next(true);
  },

  siblingMethod() {

  },
};

export default home;
