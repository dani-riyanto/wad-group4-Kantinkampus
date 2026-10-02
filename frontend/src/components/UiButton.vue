<script setup>
defineProps({
  type: { type: String, default: 'button' },
  disabled: { type: Boolean, default: false }
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="group relative inline-flex cursor-pointer select-none items-center justify-center overflow-hidden whitespace-nowrap bg-primary px-10 py-2.5 text-sm font-semibold text-white transition-colors duration-300 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
  >
    <span
      class="relative inline-flex items-center transition-transform duration-300 ease-out group-hover:-translate-x-3 motion-reduce:group-hover:translate-x-0"
    >
      <slot />
      <svg
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="pointer-events-none absolute left-full top-1/2 ml-2 h-4 w-4 -translate-x-1 -translate-y-1/2 opacity-0 transition-all duration-300 ease-out group-hover:translate-x-0 group-hover:opacity-100 motion-reduce:transition-none"
      >
        <path d="M5 12h14M13 6l6 6-6 6" />
      </svg>
    </span>
  </button>
</template>
