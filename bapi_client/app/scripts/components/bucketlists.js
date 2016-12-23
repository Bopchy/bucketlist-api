const bucketlists = {
  template: '#bucketlists',
  data():{
    name: undefined
  },
  methods: {
    addBucketlist() {
      axios.post('http://localhost:5000/bucketlists/',{
        name: this.name
      })
    }
  }
}
