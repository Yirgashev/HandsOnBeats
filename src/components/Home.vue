<template>
  <div>
    <div>
      <button id="startButton" @click="$emit('start')">Start The Game</button>
    </div>
    <div>
      <button @click="$emit('view-rank')">View Rank</button>
    </div>
  </div>
</template>

<script setup>
// import { defineEmits } from 'vue'

const $emit = defineEmits(["start", "view-rank"]);
</script>

<style scoped>

button {
  margin: 10px;
}

#startButton {
  font-size: large;
}

</style>
