<template>
  <div class="container">
    <GameInfo @return-home="$emit('return-home')" />
    <div class="imgouter">
      <div class="left_div">
        <video id="v"></video>
        <img v-if="this.gameDiff === 0" id="img-gesture" :src="imgData" />
      </div>
      <canvas
        id="photo-canvas"
        :width="vWidth"
        :height="vHeight"
        style="display: none"
      ></canvas>
      <!-- <img ref="photo" alt="photo" class="right_div" :src="imgData" /> -->
    </div>
    <RhythmVis />
    <EndBanner v-if="this.isEnd" />
  </div>
</template>

<script setup>
import RhythmVis from "./RhythmVis.vue";
import GameInfo from "./GameInfo.vue";
import EndBanner from "./EndBanner.vue";

const $emit = defineEmits(["return-home"]);
</script>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  data() {
    return {
      videoPlaying: false,
      // vWidth 和 vHeight 如果设为 0， canvas.toDataUrl() 返回为'data:'，进而导致与后端通信失败
      // 原因是在 canvas.toDataUrl() 之前程序还未修改完 canvas 的长宽
      vWidth: 600,
      vHeight: 480,
      imgData: "",
      thisContext: null,
      thisVideo: null,
      thisCanvas: null,
      interval: "",
      scoreAdd: 10,
    };
  },
  computed: {
    ...mapState([
      "timeSpace",
      "gameDiff",
      "isPaused",
      "isEnd",
      "gameStatus",
      "targetGesture",
      "identifiedGesture",
      "effectVisible",
      "effectGreat",
    ]),
  },
  watch: {
    // 当 isPaused 发生变化时会自动执行下面内容
    // 建议把实现写在 method 里，这里直接调用即可
    isPaused: {
      handler(newVal) {
        console.log("isPaused changed.");
        if (this.isPaused) {
          clearInterval(this.interval);
        } else {
          if (this.gameStatus == 2) {
            this.start_photo();
          }
        }
      },
    },
    gameStatus: {
      handler() {
        if (this.gameStatus != 2) {
          clearInterval(this.interval);
        }
      },
    },
    isEnd: {
      handler() {
        if (this.isEnd) {
          clearInterval(this.interval);
          // this.stopNavigator();
        }
      },
    },
    targetGesture: {
      handler() {
        // 清除效果图片
        this.$store.commit("change_effect_visible", false);
        // 当简单模式下才会显示手势图片
        if (this.gameDiff === 0) {
          this.changeGestureImg();
        }
      },
    },
  },
  methods: {
    upload_img(imgStr) {
      let _this = this;
      let arr = imgStr.split(";base64,");
      let suffix = arr[0].split("/")[1];
      let base64str = arr[1];
      let data = {
        image: base64str,
        suffix: suffix,
      };
      axios
        .post("http://127.0.0.1:8000/base64file", data)
        .then(function (response) {
          console.log(response.data);
          _this.$store.commit(
            "change_identified_gesture",
            response.data["gesture_recognition_result"]
          );
          _this.$store.commit("change_effect_visible", true);
          _this.updateScore();
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    take_pic() {
      if (this.videoPlaying) {
        let canvas = document.getElementById("photo-canvas");
        let v = document.getElementById("v");
        this.vWidth = v.videoWidth;
        this.vHeight = v.videoHeight;
        // console.log(canvas.width);
        // console.log(this.vWidth);
        canvas.getContext("2d").drawImage(v, 0, 0);
        let data = canvas.toDataURL("image/jpeg", 0.8); // ERROR: data is undefined
        // console.log(data);
        // this.imgData = data;
        this.upload_img(data);
        // 以下写法会导致游戏结束后，但post请求仍在继续的问题
        // this.interval = setInterval(() => {
        //   this.upload_img(data);
        // }, 3000);
      }
    },
    start_photo() {
      var _this = this;
      this.thisCanvas = document.getElementById("photo-canvas");
      this.thisContext = this.thisCanvas.getContext("2d");
      this.thisVideo = document.getElementById("v");

      // 老的浏览器可能根本没有实现 mediaDevices，所以我们可以先设置一个空的对象
      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
      }
      if (navigator.mediaDevices.getUserMedia === undefined) {
        navigator.mediaDevices.getUserMedia = function (constraints) {
          // 首先，如果有getUserMedia的话，就获得它
          var getUserMedia =
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.msGetUserMedia;
          // 一些浏览器根本没实现它 - 那么就返回一个error到promise的reject来保持一个统一的接口
          if (!getUserMedia) {
            return Promise.reject(
              new Error("getUserMedia is not implemented in this browser")
            );
          }
          // 否则，为老的navigator.getUserMedia方法包裹一个Promise
          return new Promise(function (resolve, reject) {
            getUserMedia.call(navigator, constraints, resolve, reject);
          });
        };
      }
      const constraints = {
        video: true,
        audio: false,
      };

      let promise = navigator.mediaDevices.getUserMedia(constraints);
      promise.then((stream) => {
        // 旧的浏览器可能没有srcObject
        if ("srcObject" in _this.thisVideo) {
          _this.thisVideo.srcObject = stream;
        } else {
          // 防止在新的浏览器里使用它，应为它已经不再支持了
          _this.thisVideo.src = window.URL.createObjectURL(stream);
        }
        _this.thisVideo.onloadedmetadata = function (e) {
          _this.thisVideo.play();
          _this.videoPlaying = true;

          // 设置一段时间的延迟，使得post请求的频率与手势变化的频率一致
          setTimeout(() => {
            _this.interval = setInterval(() => {
              _this.take_pic();
            }, _this.timeSpace);
          }, _this.timeSpace * 0.4);
          // _this.interval = setInterval(() => {
          //   _this.take_pic();
          // }, _this.timeSpace);
        };
      });
    },
    // 关闭摄像头
    stopNavigator() {
      this.thisVideo.srcObject.getTracks()[0].stop();
    },
    updateScore() {
      if (this.identifiedGesture === this.targetGesture) {
        this.$store.commit("update_score", this.scoreAdd);
        this.$store.commit("change_effect_great", true);
      } else {
        this.$store.commit("change_effect_great", false);
      }
    },
    changeGestureImg() {
      if (this.targetGesture !== "") {
        this.imgData = "../static/gestures/" + this.targetGesture + ".jpg";
      }
    },
  },
  created() {},
  mounted() {
    this.$nextTick(function () {
      // 仅在整个视图都被渲染之后才会运行的代码
      this.start_photo();
      // 以下写法会导致 video 重复加载的问题
      // setInterval(() => {
      //         this.start_photo();
      //       }, 1000);
    });
  },
  components: {
    GameInfo,
    RhythmVis,
  },
};
</script>

<style>
body {
  width: 100%;
  height: 100%;
}

.imgouter {
  display: block;
  height: 70%;
  /* height: 80px; */
  /* width: 30%; */
  position: relative;
  /* right: 10vw; */
  /* top: 10vh; */
  z-index: 1;
}

.left_div,
.right_div {
  position: relative;
  margin: 0 auto;
  display: flex;
  float: left;

  /* top: -10vh; */
  /* left: 10%; */
  transform: scale(0.7, 0.7);
}

#v {
  /* width: 20%;
  height: 10%; */
  object-fit: cover;
}

#img-gesture {
  position: absolute;
  z-index: 2;
  right: 0;
  bottom: -50%;
  transform: scale(0.145);
}

/* .msg {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 10vh;
  font-size: 30px;
} */
</style>
