import axios from 'axios';

const editBucketlistItem = {
  template: '#editBucketlistItem',
  data() {
    return {
      name: undefined,
      doneYes: undefined,
      doneNo: undefined,
      responseMessage: "You can either change your item's name or done status to yes."
    };
  },
  methods: {
    editBucketlistItem(input) {
      const id = this.$route.params.bucketlistId
      const itemId = this.$route.params.itemid
      if (this.name || this.doneYes || this.doneNo) {
        name = this.name;
        let done;
        if (this.doneYes) {
          done = this.doneYes;
        } else if (this.doneNo) {
          done = this.doneNo;
        }
        axios.put('http://localhost:5000/bucketlists/' + id + '/items/' + itemId, {
            name: name,
            done: done,
          })
          .then((response) => {
            this.name = undefined;
            this.doneYes = undefined;
            this.doneNo = undefined;
            this.responseMessage = response.data.message;
            this.$router.push({
              name: 'home'
            })
          })
      }
    }
  },
};

export default editBucketlistItem;
