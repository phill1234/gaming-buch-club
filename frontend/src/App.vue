<template>
  <metainfo>
    <template v-slot:title="{ content }"
    >{{ content ? `${content}` : `SITE_NAME` }}
    </template>
  </metainfo>
  <NavBar />
  <CookieBanner />
  <router-view />
</template>
<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
import { useMeta } from 'vue-meta'
import CookieBanner from '@/components/CookieBanner.vue'

useMeta({ title: 'Gaming Buch Club' })
</script>
<style></style>
