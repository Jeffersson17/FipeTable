<template>
  <v-app>
    <v-main>
      <PriceFipeTable />
    </v-main>
  </v-app>
</template>

<script>
import PriceFipeTable from './components/PriceFipeTable.vue';

export default {
  name: 'App',

  components: {
    PriceFipeTable,
  },
};
</script>
