<script setup>
import { reactive, ref } from 'vue'
import SectionHeading from './SectionHeading.vue'
import UiButton from './UiButton.vue'
import { createMenu } from '../services/api.js'

const emit = defineEmits(['menu-added'])

const form = reactive({
  nama: '',
  harga: '',
  kategori: 'Makanan',
  tersedia: true
})

const isSubmitting = ref(false)
const serverError = ref('')

const labelClass = 'mb-2 block text-[15px] leading-[23px] text-muted'
const fieldClass = 'w-full appearance-none border border-border bg-white px-4 py-2.5 text-base text-primary placeholder:text-muted focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary'

const handleSubmit = async () => {
  if (!form.nama || form.harga <= 0) {
    alert('Nama dan Harga menu wajib diisi dengan benar!')
    return
  }

  isSubmitting.value = true
  serverError.value = ''

  try {
    const payload = {
      nama: form.nama,
      harga: Number(form.harga),
      kategori: form.kategori,
      tersedia: form.tersedia
    }
    
    await createMenu(payload)
    
    // Reset form setelah berhasil
    form.nama = ''
    form.harga = ''
    form.kategori = 'Makanan'
    form.tersedia = true
    
    // Beri tahu App.vue bahwa menu baru telah ditambahkan
    emit('menu-added')
    
  } catch (err) {
    serverError.value = err.message
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="border border-border bg-surface-1 p-5 mt-6">
    <SectionHeading eyebrow="Formulir" title="Tambah Menu Baru" subtitle="Daftarkan menu ke database" level="h3" class="border-b border-border pb-4" />

    <p v-if="serverError" role="alert" class="mt-4 border border-danger bg-white p-3 text-[15px] leading-[23px] text-danger">{{ serverError }}</p>

    <form @submit.prevent="handleSubmit" class="mt-4 space-y-4" novalidate>
      <div>
        <label for="nama" :class="labelClass">Nama Menu</label>
        <input id="nama" v-model="form.nama" type="text" placeholder="Contoh: Nasi Goreng Spesial" :class="fieldClass" required />
      </div>

      <div>
        <label for="harga" :class="labelClass">Harga (Rp)</label>
        <input id="harga" v-model="form.harga" type="number" placeholder="Contoh: 25000" :class="fieldClass" required />
      </div>

      <div>
        <label for="kategori" :class="labelClass">Kategori</label>
        <select id="kategori" v-model="form.kategori" :class="fieldClass">
          <option value="Makanan">Makanan</option>
          <option value="Minuman">Minuman</option>
          <option value="Cemilan">Cemilan</option>
        </select>
      </div>

      <div class="flex items-center gap-2">
        <input id="tersedia" v-model="form.tersedia" type="checkbox" class="w-4 h-4 cursor-pointer" />
        <label for="tersedia" class="text-[15px] text-primary cursor-pointer">Menu Tersedia</label>
      </div>

      <UiButton type="submit" :disabled="isSubmitting" class="w-full mt-2">
        {{ isSubmitting ? 'Menyimpan...' : 'Simpan Menu (POST)' }}
      </UiButton>
    </form>
  </div>
</template>