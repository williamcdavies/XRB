import { defineConfig } from 'vite'
import path             from 'path'
import tailwindcss      from '@tailwindcss/vite'
import vue              from '@vitejs/plugin-vue'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
