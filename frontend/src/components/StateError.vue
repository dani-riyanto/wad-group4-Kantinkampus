<script setup>
defineProps({
  errorMessage: { type: String, default: 'Gagal mengambil data dari server.' }
})
defineEmits(['retry'])
</script>

<template>
  <div class="py-10 px-6 text-center text-red-300 bg-red-950/20 border border-red-900/40 rounded-xl my-4">
    <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 mx-auto mb-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
    <p class="text-sm font-semibold text-white mb-1">Terjadi Kesalahan Server</p>
    <p class="text-xs mb-4 text-red-400">{{ errorMessage }}</p>
    <button @click="$emit('retry')"
      class="bg-red-800 hover:bg-red-700 text-white text-xs font-semibold px-4 py-2 rounded-lg transition duration-150 focus-visible:ring-2 focus-visible:ring-white">
      Coba Lagi (Retry)
    </button>
  </div>
</template>
