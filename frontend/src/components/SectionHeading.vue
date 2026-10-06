<script setup>
import { computed } from 'vue'

const props = defineProps({
  eyebrow: { type: String, required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  level: { type: String, default: 'h2' },
  tone: { type: String, default: 'light' }
})

const eyebrowClass = computed(() => (props.tone === 'dark' ? 'text-white' : 'text-primary'))
const titleClass = computed(() => (props.tone === 'dark' ? 'text-white' : 'text-primary'))
const subtitleClass = computed(() => (props.tone === 'dark' ? 'text-on-dark' : 'text-body'))
</script>

<template>
  <div>
    <span class="block text-[13px] uppercase tracking-[0.25em]" :class="eyebrowClass">{{ eyebrow }}</span>
    <component :is="level" class="mt-2.5 font-serif text-[24px] font-normal leading-[32px] lg:text-[26px] lg:leading-[34px]"
      :class="titleClass">{{ title }}</component>
    <p v-if="subtitle" class="mt-3 max-w-[809px] text-base leading-[26px]" :class="subtitleClass">{{ subtitle }}</p>
    <slot />
  </div>
</template>
