import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Listen on all addresses (0.0.0.0)
    port: 5177, // Using 5177 since 5176 might be busy
    strictPort: false,
    proxy: {
      '/search': 'http://127.0.0.1:8000',
      '/ingest': 'http://127.0.0.1:8000',
      '/uploads': 'http://127.0.0.1:8000',
    }
  },
})
