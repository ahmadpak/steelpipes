<template>
  <button v-on:click="count++" class="btn btn-primary">Click count — {{ count }}</button>
</template>

<script>
export default {
  props: ["count"],
  data: function() {
    return {
      count: 0
    };
  }
};
</script>
