<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  user: { type: Object, default: null },
  busy: Boolean,
  error: { type: String, default: '' },
  message: { type: String, default: '' },
  users: { type: Array, default: () => [] }
})

const emit = defineEmits(['login', 'logout', 'update-profile', 'create-user', 'delete-user'])

const credentials = reactive({ username: '', password: '' })
const profile = reactive({ displayName: '' })
const newUser = reactive({ username: '', password: '12345' })

watch(
  () => props.user,
  user => {
    profile.displayName = user?.display_name || ''
    credentials.username = ''
    credentials.password = ''
  },
  { immediate: true }
)

const submitLogin = () => {
  emit('login', { ...credentials })
}

const submitProfile = () => {
  emit('update-profile', profile.displayName.trim())
}

const submitNewUser = () => {
  emit('create-user', {
    username: newUser.username.trim(),
    password: newUser.password
  })
}
</script>

<template>
  <section class="container py-6">
    <div class="border border-border bg-surface-1 p-5 sm:p-6">
      <div class="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.12em] text-muted">Akun dan otorisasi</p>
          <h2 class="mt-1 font-serif text-2xl text-primary">
            {{ user ? `Halo, ${user.display_name}` : 'Masuk ke akun' }}
          </h2>
          <p class="mt-1 text-sm text-muted">
            {{ user ? `${user.username} · role ${user.role}` : 'Login untuk mengelola akun demo.' }}
          </p>
        </div>
        <button
          v-if="user"
          type="button"
          class="border border-border bg-white px-4 py-2 text-sm font-semibold text-primary hover:border-primary"
          :disabled="busy"
          @click="emit('logout')"
        >
          Keluar
        </button>
      </div>

      <p v-if="error" role="alert" class="mt-4 border border-danger bg-white p-3 text-sm text-danger">
        {{ error }}
      </p>
      <p v-if="message" role="status" class="mt-4 border border-success bg-white p-3 text-sm text-success">
        {{ message }}
      </p>

      <p v-if="!user && busy" class="mt-5 text-sm text-muted" role="status">
        Memeriksa sesi...
      </p>

      <form v-else-if="!user" class="mt-5 grid gap-4 sm:grid-cols-3" @submit.prevent="submitLogin">
        <label class="block text-sm text-muted">
          Username
          <input
            v-model="credentials.username"
            class="mt-1 w-full border border-border bg-white px-3 py-2 text-primary focus:border-primary focus:outline-none"
            autocomplete="username"
            required
          />
        </label>
        <label class="block text-sm text-muted">
          Password
          <input
            v-model="credentials.password"
            class="mt-1 w-full border border-border bg-white px-3 py-2 text-primary focus:border-primary focus:outline-none"
            type="password"
            autocomplete="current-password"
            required
          />
        </label>
        <div class="flex items-end">
          <button
            type="submit"
            class="w-full bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-[#203a56] disabled:opacity-60"
            :disabled="busy"
          >
            {{ busy ? 'Memproses...' : 'Login' }}
          </button>
        </div>
        <p class="text-xs text-muted sm:col-span-3">
          Akun demo: admin, userA, userB, userC — password 12345. Admin membuat akun user melalui panel ini.
        </p>
      </form>

      <div v-else class="mt-5 grid gap-6 lg:grid-cols-2">
        <form class="space-y-3" @submit.prevent="submitProfile">
          <h3 class="font-semibold text-primary">Profil saya</h3>
          <label class="block text-sm text-muted">
            Nama tampilan
            <input
              v-model="profile.displayName"
              class="mt-1 w-full border border-border bg-white px-3 py-2 text-primary focus:border-primary focus:outline-none"
              minlength="2"
              maxlength="100"
              required
            />
          </label>
          <button
            type="submit"
            class="bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-[#203a56] disabled:opacity-60"
            :disabled="busy"
          >
            Simpan profil
          </button>
        </form>

        <form v-if="user.role === 'admin'" class="space-y-3" @submit.prevent="submitNewUser">
          <h3 class="font-semibold text-primary">Buat akun user</h3>
          <label class="block text-sm text-muted">
            Username baru
            <input
              v-model="newUser.username"
              class="mt-1 w-full border border-border bg-white px-3 py-2 text-primary focus:border-primary focus:outline-none"
              minlength="3"
              maxlength="50"
              autocomplete="off"
              required
            />
          </label>
          <label class="block text-sm text-muted">
            Password awal
            <input
              v-model="newUser.password"
              class="mt-1 w-full border border-border bg-white px-3 py-2 text-primary focus:border-primary focus:outline-none"
              type="password"
              minlength="1"
              autocomplete="new-password"
              required
            />
          </label>
          <p class="text-xs text-muted">Role user. Untuk latihan, password yang disepakati adalah 12345.</p>
          <button
            type="submit"
            class="border border-primary px-4 py-2 text-sm font-semibold text-primary hover:bg-white disabled:opacity-60"
            :disabled="busy"
          >
            Buat akun
          </button>
        </form>

        <p v-else class="text-sm text-muted">
          Anda hanya dapat mengubah profil sendiri. Akun user lain tidak dapat diubah.
        </p>
      </div>

      <div v-if="user?.role === 'admin'" class="mt-6 border-t border-border pt-5">
        <h3 class="font-semibold text-primary">Akun user ({{ users.length }})</h3>
        <p v-if="users.length === 0" class="mt-2 text-sm text-muted">Belum ada akun user.</p>
        <ul v-else class="mt-3 divide-y divide-border border-y border-border bg-white">
          <li
            v-for="account in users"
            :key="account.id"
            class="flex flex-wrap items-center justify-between gap-3 px-3 py-3"
          >
            <div>
              <p class="font-semibold text-primary">{{ account.username }}</p>
              <p class="text-sm text-muted">{{ account.display_name }} · {{ account.role }}</p>
            </div>
            <button
              type="button"
              class="border border-danger px-3 py-1.5 text-sm font-semibold text-danger hover:bg-red-50"
              :disabled="busy"
              @click="emit('delete-user', account)"
            >
              Hapus akun
            </button>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>
