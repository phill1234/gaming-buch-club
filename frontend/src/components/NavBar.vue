<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Gaming Buch Club</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0"></ul>
        <button class="btn btn-outline-success" type="submit" @click="login">
          Login
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { loginWithRedirect } = useAuth0();

const login = () => {
  loginWithRedirect();
};
</script>
