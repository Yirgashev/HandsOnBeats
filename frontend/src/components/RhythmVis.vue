<template>
  <div class="animate">
    <div class="circle">
      <svg class="main-circle" id="main-circle">
        <g id="circle-g">
          <circle id="circle-obj"></circle>
          <text id="circle-text"></text>
          <path id="circle-path"></path>
        </g>
        <g id="circle-g2">
          <circle id="circle-obj2"></circle>
          <text id="circle-text2"></text>
        </g>
      </svg>
    </div>
    <img v-if="effectVisible" id="effect-img" :src="imgData" />
  </div>
</template>

<script>
import * as d3 from "d3";
import { mapState } from "vuex";

export default {
  data() {
    return {
      context: [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
      ],
      interval: "",
      index: 0,
      width: window.innerWidth,
      height: window.innerHeight,
      imgData: "",
    };
  },
  computed: {
    ...mapState([
      "gameStatus",
      "gameDiff",
      "isPaused",
      "isEnd",
      "targetGesture",
      "timeSpace",
      "effectVisible",
      "effectGreat",
    ]),
  },
  watch: {
    width(newVal, oddVal) {
      this.width = newVal;
    },
    height(newVal, oddVal) {
      this.height = newVal;
    },
    isPaused: {
      handler() {
        if (this.isPaused) {
          this.stop_game();
        } else {
          this.start_game();
        }
      },
    },
    gameStatus: {
      handler() {
        // 回到主页即结束游戏
        if (this.gameStatus != 2) {
          this.stop_game();
        }
      },
    },
    effectVisible: {
      handler() {
        if (this.effectVisible) {
          this.pick_img();
        } else {
          this.clear_img();
        }
      },
    },
  },
  methods: {
    read_data() {
      // 视关卡难度读取对应的数据内容
      if (this.gameStatus === 2 && this.gameDiff === 2) {
        // Advanced: 随机打乱数组
        this.context.sort(() => Math.random() - 0.5);
      }
    },
    draw_rhythm(text1, text2) {
      const width = this.width * 0.8;
      const height = this.height * 0.8;

      // this.svg = d3.select("#main-circle");
      // const pane = d3.select("#circle-g");

      var arcGenerator = d3
        .arc()
        .innerRadius(height * 0.2)
        .outerRadius(height * 0.23)
        .startAngle(0);

      d3.select("#circle-path")
        .datum({ endAngle: 2 * Math.PI })
        .attr("class", "arc")
        .attr("fill", "#E49A2B")
        .attr("transform", `translate(${width * 0.17}, ${height * 0.3})`)
        .attr("fill-opacity", 0.8)
        .attr("stroke-width", 1);

      d3.select("#circle-path")
        .transition()
        .duration(this.timeSpace)
        .attrTween("d", function (d) {
          var compute = d3.interpolate(0, Math.PI * 2);
          return function (t) {
            d.endAngle = compute(t);
            return arcGenerator(d);
          };
        });

      // 主圆形 main-circle
      // 绘制圆形
      d3.select("#circle-obj")
        .attr("stroke", "#FDF2CC")
        .attr("cx", width * 0.17) // 调整 x 坐标
        .attr("cy", height * 0.3) // 调整 y 坐标
        .attr("r", height * 0.2)
        .attr("fill", "#FFE5A4")
        .attr("fill-opacity", 1)
        .attr("stroke-width", 1);

      // 绘制文字
      d3.select("#circle-text")
        .text(text1)
        .attr("x", `${width * 0.13}`) // 调整 x 坐标
        .attr("y", `${height * 0.355}`) // 调整 y 坐标
        .attr("class", "character")
        .attr("font-size", 100);

      // 绘制圆形
      d3.select("#circle-obj2")
        .attr("stroke", "#EFDF2CC")
        .attr("cx", width * 0.4) // 调整 x 坐标
        .attr("cy", height * 0.3) // 调整 y 坐标
        .attr("r", height * 0.1)
        .attr("fill", "#FDF2CC")
        .attr("fill-opacity", 1)
        .attr("stroke-width", 1);

      // 绘制文字
      d3.select("#circle-text2")
        .text(text2)
        .attr("x", `${width * 0.38}`) // 调整 x 坐标
        .attr("y", `${height * 0.34}`) // 调整 y 坐标
        .attr("class", "character")
        .attr("color", "#6C6C6C")
        .attr("font-size", 60);
    },
    start_game() {
      this.interval = setInterval(() => {
        console.log(this.context[this.index]);
        this.draw_rhythm(
          this.context[this.index],
          this.index + 1 > this.context.length
            ? ""
            : this.context[this.index + 1]
        );
        this.$store.commit("change_target_gesture", this.context[this.index]);
        this.index++;
        if (this.index >= this.context.length) {
          // 在最后一个字母的时间结束后才结束游戏
          setTimeout(() => {
            this.stop_game();
          }, this.timeSpace * 0.9);
        }
      }, this.timeSpace);
    },
    stop_game() {
      clearInterval(this.interval);
      this.$store.commit("end_game");
    },
    pick_img() {
      console.log("effectGreat: ", this.effectGreat);
      if (this.effectGreat) {
        this.imgData = "../static/image/effects/great.png";
      } else {
        this.imgData = "../static/image/effects/miss.png";
      }
    },
    clear_img() {
      this.imgData = "";
    },
  },
  created() {
    this.read_data();
  },
  mounted() {
    this.start_game();
  },
};
</script>

<style>
.animate {
  position: relative;
  display: flex;
  /* float:left; */
  height: 100vh;
  /* width: 100vw; */
  top: 10vh;
  z-index: 2;
  /* right: -50%; */
  /* align-items: center; */
  /* justify-content: center; */
}

/* .circle {
  width: 10em;
	height: 10em;
  border-radius: 50%;
  border: 1em solid orange;
  background: orange;
  animation: circular 3s linear infinite;
}
*/
/* .circle {

  width: 20em;
	height: 20em;
  background: orange;

  border-radius: 50%;
  transform: rotate(-45deg);
  animation: circular 3s linear infinite;
} */

.main-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  /* left: 50%; */
  /* top: 100px; */
}

.character {
  font-weight: 500;
  font-family: Arial, Helvetica, sans-serif;
  /* text-anchor: middle; */
  /* position: absolute;
  top: 50%;
  left: 50%; */
}

circle {
  position: absolute;
  display: flex;
  height: 100vh;
  width: 100vw;
  z-index: 2;
}

#effect-img {
  position: relative;
  transform: scale(0.3);
  display: flex;
}
</style>
