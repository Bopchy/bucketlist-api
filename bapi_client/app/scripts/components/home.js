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
      if (this.bapiToken) {
        console.log(this.bapiToken);
      } else {
        this.$router.push({
            name: 'sign-in',
          });
        }
      },
      // The following methods sub-object are accesible in this component events, sibling methods
      // and also in the DOM/HTML/this component's template if attached to an event eg click event
      beforeRouteEnter(to, from, next) {
          axios.get('http://localhost:5000/bucketlists/')
            .then((response) => {
              // Accesses this next before home component (represented as thisComponent) is instantiated
              next((thisComponent) => {
                // Assigning result of response to buckets
                console.log(response);
                thisComponent.buckets = response.data.bucketlists;
              })
            }).catch((err) => {
              console.log(err);
              next()
            })
        },

        siblingMethod() {

        },
    };

    export default home;
