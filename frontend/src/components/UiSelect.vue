<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  id: { type: String, required: true },
  label: { type: String, required: true },
  options: { type: Array, required: true }
})
const emit = defineEmits(['update:modelValue'])

const items = computed(() => props.options.map(o => (typeof o === 'string' ? { value: o, label: o } : o)))
</script>

<template>
  <div>
    <label :for="id" class="mb-2 block text-[15px] leading-[23px] text-muted">{{ label }}</label>
    <div class="relative">
      <select
        :id="id"
        :value="modelValue"
        @change="emit('update:modelValue', $event.target.value)"
        class="w-full appearance-none border border-border bg-white px-4 py-2.5 pr-10 text-base text-primary focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary"
      >
        <option v-for="item in items" :key="item.value" :value="item.value">{{ item.label }}</option>
      </select>
      <svg
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted"
      >
        <path d="m6 9 6 6 6-6" />
      </svg>
    </div>
  </div>
</template>
