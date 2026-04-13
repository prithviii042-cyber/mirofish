import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // In production, VITE_API_BASE_URL points to the Railway backend.
  // In development, the dev server proxy handles /api/* → localhost:5001.
  const apiBase = env.VITE_API_BASE_URL || ''

  return {
    plugins: [vue()],
    server: {
      port: 3000,
      open: true,
      proxy: {
        '/api': {
          target: 'http://localhost:5001',
          changeOrigin: true,
          secure: false
        }
      }
    },
    define: {
      __API_BASE__: JSON.stringify(apiBase)
    }
  }
})
