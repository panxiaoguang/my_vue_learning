<script setup>
import upload from "./components/upload.vue";
import hljs from 'highlight.js/lib/core'
import bash from 'highlight.js/lib/languages/bash'
hljs.registerLanguage('bash', bash)
</script>

<template>
  <n-message-provider>
    <n-config-provider :hljs="hljs">
      <upload />
    </n-config-provider>
    
  </n-message-provider>
</template>
