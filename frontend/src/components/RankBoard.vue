<template>
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

    <table>
      <tr>
        <th v-for="(item, ind) in columns" :key="ind">{{ item }}</th>
      </tr>
      <tr v-for="(item, index) in rankList" :key="index">
        <td v-for="(it, ind) in columns" :key="ind">{{ item[it] }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup>
const $emit = defineEmits(["return-home"]);
</script>

<script>
import axios from "axios";
import jquery from "jquery";

export default {
  data() {
    return {
      columns: ["rank", "id", "score", "timestamp"],
      rankList: [
        { rank: 1, ID: "A", score: 20 },
        { rank: 2, ID: "B", score: 15 },
      ],
    };
  },
  methods: {
    getRankList() {
      const _this = this;
      axios
        .post("http://127.0.0.1:8000/getRankingList")
        .then(function (response) {
          console.log(response.data);
          _this.rankList = jquery.parseJSON(response.data);
          _this.processRankList();
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    processRankList() {
      const result = [];
      for (let i=0; i<this.rankList.length; i++){
        let data = {"rank": i+1};
        result[i] = Object.assign({}, data, this.rankList[i]);
      }
      this.rankList = result;
      console.log(result);
    }
  },
  mounted() {
    this.getRankList();
  }
};
</script>

<style>
button {
  position: relative;
  /* left: -30%;
  top:30%; */
}

table {
  width: 50%;
  padding: 10%;
  border-collapse: collapse;   /* 将表格边框折叠为单一边框 */
}

th {
  text-align: center;
  padding: 15px;
}

th, td {
  border-bottom: 1px solid #ddd;
}

tr:hover {background-color: #f5f5f5;}


</style>
