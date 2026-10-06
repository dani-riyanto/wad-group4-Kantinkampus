<script setup>
defineProps({
  modelValue: { type: [Number, String], default: 1 },
  label: { type: String, required: true },
  id: { type: String, required: true },
  error: { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div>
    <label :for="id" class="mb-2 block text-[15px] leading-[23px] text-muted">{{ label }}</label>
    <div class="flex border border-border bg-white">
      <button type="button" @click="emit('update:modelValue', Math.max(1, Number(modelValue) - 1))"
        :aria-label="`Kurangi ${label}`"
        class="border-r border-border px-4 py-2.5 text-base text-primary transition-colors hover:bg-surface-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary">−</button>
      <input :id="id" :value="modelValue" @input="emit('update:modelValue', Number($event.target.value))" type="number"
        min="1"
        class="w-full min-w-0 appearance-none border-0 bg-transparent px-2 py-2.5 text-center text-base text-primary focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary" />
      <button type="button" @click="emit('update:modelValue', Number(modelValue) + 1)" :aria-label="`Tambah ${label}`"
        class="border-l border-border px-4 py-2.5 text-base text-primary transition-colors hover:bg-surface-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary">+</button>
    </div>
    <span v-if="error" class="mt-1 block text-[15px] leading-[23px] text-danger">{{ error }}</span>
  </div>
</template>
