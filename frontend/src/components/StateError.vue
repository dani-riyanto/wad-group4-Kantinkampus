<script setup>
import UiButton from './UiButton.vue'

defineProps({
  errorMessage: { type: String, default: 'Gagal mengambil data dari server.' }
})
defineEmits(['retry'])
</script>

<template>
  <div role="alert" class="border border-danger bg-white px-6 py-10 text-center">
    <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mx-auto h-10 w-10 text-danger">
      <path d="M10.3 4 2.6 17.3A2 2 0 0 0 4.3 20.3h15.4a2 2 0 0 0 1.7-3L13.7 4a2 2 0 0 0-3.4 0Z" />
      <path d="M12 9v4M12 17h.01" />
    </svg>
    <p class="mt-4 font-serif text-2xl font-bold text-primary">Terjadi kesalahan server</p>
    <p class="mt-2 text-base leading-[26px] text-danger">{{ errorMessage }}</p>
    <UiButton class="mt-6" @click="$emit('retry')">Coba lagi (Retry)</UiButton>
  </div>
</template>
