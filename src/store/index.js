import { createStore } from 'vuex';

export default createStore({
    state: {
        gameStatus: 0,   // 可以将此看作是页面的索引。0: home，1: selectDiff，2: 开始游戏，3：排行榜
        gameDiff: 0,
        isPaused: false,
        isEnd: false,
        score: 0,
        targetGesture: "",
        identifiedGesture: "",
        playerID: "Unknown",
        timeSpace: 3000,     // 间隔 3s
        effectVisible: false,
        effectGreat: false,
    },
    mutations: {
      show_home(state) {
        // 返回主页面，将所有状态恢复至初始值
				state.gameStatus = 0;
        state.score = 0;
        state.isPaused = false;
        state.isEnd = false;
			},
			show_difficulty(state) {
				state.gameStatus = 1;
        state.score = 0;
        state.isPaused = false;
        state.isEnd = false;
			},
			select_difficulty(state, payload) {
				state.gameStatus = 2;    // 进入游戏状态
				state.gameDiff = payload;    // 0: easy   1: medium   2: advanced
        state.isEnd = false;
        state.isPaused = false;
        state.score = 0;
        // 困难模式下将间隔时间缩短为 2s
        if (payload === 2) {
          state.timeSpace = 2000;
        }
			},
      changePaused(state) {
        state.isPaused = !state.isPaused;
      },
      show_rank(state) {
        state.gameStatus = 3;
      },
      end_game(state) {
        state.isEnd = true;
      },
      update_score(state, payload) {
        state.score += payload;
      },
      change_target_gesture(state, payload) {
        state.targetGesture = payload;
      },
      change_identified_gesture(state, payload) {
        state.identifiedGesture = payload;
      },
      change_playerID(state, payload) {
        state.playerID = payload;
      },
      change_time_space(state, payload) {
        state.timeSpace = payload;
      },
      change_effect_visible(state, payload) {
        state.effectVisible = payload;
      },
      change_effect_great(state, payload) {
        state.effectGreat = payload;
      }
    },
    actions: {},
    modules: {}
})
