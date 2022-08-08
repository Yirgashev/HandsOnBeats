<template>
  <div>
    <div>
      <text class="description show" v-show="this.textVisible">
        {{ this.text }}
      </text>
    </div>
    <button
      id="easyButton"
      class="button min-w-25"
      @click="$emit('easy')"
      @mouseenter="easyHover"
      @mouseleave="clearHover"
    >
      Easy
    </button>
    <button
      id="mediumButton"
      class="button min-w-25"
      @click="$emit('medium')"
      @mouseenter="mediumHover"
      @mouseleave="clearHover"
    >
      Medium
    </button>
    <button
      id="advancedButton"
      class="button min-w-25"
      @click="$emit('advanced')"
      @mouseenter="advancedHover"
      @mouseleave="clearHover"
    >
      Advanced
    </button>
    <div>
      <button class="returnButton" @click="$emit('return-home')">
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
    </div>
  </div>
</template>

<script setup>
// import { defineEmits } from 'vue'

const $emit = defineEmits(["easy", "medium", "advanced", "return-home"]);
</script>

<script>
export default {
  data() {
    return {
      easyComment: "入门级\n附有手势图片提示，第一次玩推荐",
      mediumComment: "进阶级\n按照字母顺序打出正确手势",
      advancedComment: "挑战级\n速度加快，打乱顺序",
      text: "",
      textVisible: false,
    };
  },
  methods: {
    easyHover() {
      this.text = this.easyComment;
      this.textVisible = true;
    },
    mediumHover() {
      this.text = this.mediumComment;
      this.textVisible = true;
    },
    advancedHover() {
      this.text = this.advancedComment;
      this.textVisible = true;
    },
    clearHover() {
      this.textVisible = false;
    },
  },
};
</script>

<style scoped>
.button {
  margin: 10px;
}

#easyButton {
  color: #9acd32;
}

#mediumButton {
  color: orange;
}

#advancedButton {
  color: #ff4500;
}

.returnButton:hover {
  color: white;
  background-color: #646cff;
  transition: background-color 0.25s;
}

.description {
  color: grey;
  transition: all 1s;
  white-space:pre-wrap;
}

.show {
  animation: show-detail 0.25s ease-in forwards;
}

@keyframes show-detail {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

</style>
