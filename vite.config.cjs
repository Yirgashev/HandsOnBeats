import {
  defineConfig
} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // publicPath: "/HandOnBeats/",
})

// module.exports = {};

// module.exports = {
//   devServer: {
//     proxy: {
//       '/api': {
//         // 此处的写法，目的是为了 将 /api 替换成 https://www.baidu.com/
//         target: 'https://www.baidu.com/',
//         // 允许跨域
//         changeOrigin: true,
//         ws: true,
//         pathRewrite: {
//           '^/api': ''
//         }
//       }
//     }
//   }
// }
