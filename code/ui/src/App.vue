<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <RouterView />
  <RouterLink to="/">Home</RouterLink>
  <RouterLink to="/about">About</RouterLink>
</template>
