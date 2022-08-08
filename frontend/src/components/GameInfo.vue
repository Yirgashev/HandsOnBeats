<template>
  <div class="button_top">
    <button
      class="returnButton top_distance"
      @click="this.$store.commit('show_difficulty')"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="currentColor"
        class="bi bi-house-door"
        viewBox="0 0 16 16"
      >
        <path
          d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146zM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4H2.5z"
        />
      </svg>
    </button>

    <div class="time2 top_distance" ref="startTimer">
      <!-- <h2 id="timer"> 02:15 </h2> -->
      <strong id="timer"> {{ timer }} </strong>
    </div>

    <button
      class="pause top_distance"
      @click="this.isPaused ? this.start_timer() : this.pause_timer()"
    >
      <svg
        v-if="!this.isPaused"
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="currentColor"
        class="bi bi-pause-circle"
        viewBox="0 0 16 16"
      >
        <path
          d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
        />
        <path
          d="M5 6.25a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5zm3.5 0a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5z"
        />
      </svg>
      <svg
        v-if="this.isPaused"
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="currentColor"
        class="bi bi-play-circle"
        viewBox="0 0 16 16"
      >
        <path
          d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
        />
        <path
          d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445z"
        />
      </svg>
    </button>
    <div class="score">{{ this.score }}</div>
  </div>
</template>

<script setup>
// import { defineEmits } from 'vue'
import { mapState } from "vuex";

// const $emit = defineEmits(["return-home"]);
</script>

<script>
import { ref } from "vue";

export default {
  data() {
    return {
      timer: ref("00:00"),
      minutes: 0,
      seconds: 0,
      interval: "",
      // scoreAdd: 10,
    };
  },
  computed: {
    ...mapState([
      "gameStatus",
      "gameDiff",
      "isPaused",
      "isEnd",
      "score",
      "targetGesture",
      "identifiedGesture",
    ]),
  },
  watch: {
    isEnd: {
      handler() {
        if (this.isEnd) {
          this.pause_timer();
        }
      },
    },
    // targetGesture: {
    //   handler() {
    //     if (!this.isEnd) {
    //       console.log("identifiedGesture changed. ")
    //       this.updateScore();
    //     }
    //   }
    // }
    // gameStatus: {
    //   handler() {
    //     console.log(this.gameStatus);
    //     if (this.gameStatus == 2) {
    //       this.timer = ref("00:00");
    //       this.minutes = 0;
    //       this.seconds = 0;
    //       this.start_timer();
    //     } else {
    //       this.pause_timer();
    //     }
    //   },
    // },
  },
  methods: {
    run_timer() {
      this.seconds += 1;
      if (this.seconds >= 60) {
        this.seconds = 0;
        this.minutes = this.minutes + 1;
      }
      this.timer =
        (this.minutes < 10 ? "0" + this.minutes : this.minutes) +
        ":" +
        (this.seconds < 10 ? "0" + this.seconds : this.seconds);
    },
    pause_timer() {
      clearInterval(this.interval);
      if (!this.isPaused) {
        this.$store.commit("changePaused");
      }
    },
    start_timer() {
      // 开始计时器
      if (!this.isEnd) {
        this.interval = setInterval(() => this.run_timer(), 1000);
        if (this.isPaused) {
          // 避免游戏开始但出于暂停的状态
          this.$store.commit("changePaused");
        }
      }
    },
    // updateScore() {
    //   if (this.identifiedGesture === this.targetGesture) {
    //     this.$store.commit("update_score", this.scoreAdd);
    //   }
    // }
  },
  mounted() {
    // this.timer = ref("00:00");
    // this.minutes = 0;
    // this.seconds = 0;
    console.log(this.isEnd);
    this.start_timer();
  },
};
</script>

<style scoped>
.container {
  height: 20%;
  width: 100%;
  display: flex;
  text-align: center;
}

/* .returnButton { */
/* position: absolute; */
/* left: 20%; */
/* } */

/* .pause { */
/* position: absolute; */
/* left: 43%; */
/* } */

/* #timer { */
/* position: absolute; */
/* text-align: center; */
/* margin: 1% auto; */
/* left: 50%; */
/* } */

.button_top {
  height: 100px;
  width: 100vw;
  position: relative;
  display: flex;
  flex-direction: row;
  /* justify-content:center;*/
  justify-content: space-around;
  align-items: center;
  /* justify-content: center; */
  top: -40%;
  /* transform : translate(0, -100px); */
}
.score {
  position: relative;
  display: block;
  width: 40vw;
  font-size: 40px;
  font-family: Marker Felt, Brush Script MT, Impact, Apple Chancery,
    "Times New Roman", Times, serif;
}
.time2 {
  /* width: inherit; */
  width: 80px;
  text-align: center;
}

.returnButton,
.pause,
.time2 {
  margin: 0;
  /* position: relative; */
  float: left;
}
</style>
