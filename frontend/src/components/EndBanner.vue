<template>
  <div class="banner visible">
    <div>
      <p class="text_describe">Well Done!</p>
    </div>
    <div>
      <p class="text_notice">Please Enter Your ID:</p>
      <input v-model="this.name" />
    </div>
    <button class="attribute__button" @click="commitAndHome">Confirm</button>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  props: {
    isVisible: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    ...mapState([
      "isPaused",
      "isEnd",
      "gameStatus",
      "targetGesture",
      "identifiedGesture",
      "score",
      "playerID"
    ]),
  },
  data() {
    return {
      name: "Unknown",
    };
  },
  methods: {
    commitAndHome() {
      this.$store.commit("change_playerID", this.name);
      const data = {"id": this.playerID, "score": this.score};
      console.log(data);
      axios
        .post("http://127.0.0.1:8000/saveScore", data)
        .then(function (response) {
          console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        });
      this.$store.commit("show_home");
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../style.css";

.banner {
  position: absolute;
  top: -100%;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  background-color: rgba(213 64 98 / 70%);
  transition: top 1s;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.visible {
  animation-name: scrolling;
  animation-duration: 1s;
  top: 0;
  transition: top 1s;
}
.attribute {
  &__button {
    margin-top: 2em;
    animation: appear 3s ease-in-out;
  }
}

.text_describe {
  font-weight: bolder;
  font-size: 5em;
  color: orange;
  // 不是很好看的文字描边
  // -webkit-text-stroke: 0.01em;
  // -webkit-text-stroke-color: #FFF;
}

.text_notice {
  color: white;
  font-size: 2em;
  font-weight: bold;
}
</style>
