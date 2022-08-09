<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Home from "./components/Home.vue";
import SelectDifficulty from "./components/SelectDifficulty.vue";
import GamePage from "./components/GamePage.vue";
import { mapState } from "vuex";
import RhythmVis from "./components/RhythmVis.vue";
import RankBoard from "./components/RankBoard.vue";
import EndBanner from "./components/EndBanner.vue";

</script>

<template>
  <div>
    <div v-if="this.gameStatus === 1 || this.gameStatus === 0">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
      <h1>Hands on Beats</h1>
    </div>
    <Home v-if="this.gameStatus === 0" class="normal-bg" @start="showDifficulty" @view-rank="showRank"/>
    <RankBoard v-if="this.gameStatus === 3" @return-home="showHome"/>
    <SelectDifficulty
      v-if="this.gameStatus === 1"
      class="normal-bg"
      @easy="selectDifficulty(0)"
      @medium="selectDifficulty(1)"
      @advanced="selectDifficulty(2)"
      @return-home="showHome"
    />
    <GamePage
      v-if="this.gameStatus === 2"
      @return-home="showDifficulty"
    />
    <!-- <RhythmVis v-if="this.gameStatus === 2"/> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
    };
  },
  computed: {
    ...mapState(["gameStatus", "gameDiff"]),
  },
  methods: {
    showHome() {
      this.$store.commit("show_home");
    },
    showDifficulty() {
      this.$store.commit("show_difficulty");
    },
    selectDifficulty(num) {
      this.$store.commit("select_difficulty", num);
    },
    showRank() {
      this.$store.commit("show_rank");
    }
  },
};
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
