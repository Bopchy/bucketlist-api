const home = {
  template: '#home',
  data() {
    return {
      message: 'You are at home now',
    };
  },
  // other Vue component events: created, beforeMount, mounted, beforeUpdate, updated
  beforeCreate() {
    // Do anything here eg. fetch new data, verify some things etc
    console.log(this.bapiToken);
  },
  // The following methods sub-object are accesible in this component events, sibling methods
  // and also in the DOM/HTML/this component's template if attached to an event eg click event
  methods: {
    changeMessage() {
      this.message = 'The message has been changed';
    },
    siblingMethod() {

    },
  },
};

export default home;
