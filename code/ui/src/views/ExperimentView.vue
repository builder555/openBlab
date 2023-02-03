<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "vue-chartjs";
const chartConfig = {
  data: {
    labels: [
      "10:00:00",
      "10:00:02",
      "10:00:04",
      "10:00:06",
      "10:00:08",
      "10:00:10",
      "10:00:12",
    ],
    datasets: [
      {
        label: "Temperature",
        backgroundColor: "#f87979",
        data: [36.9, 37, 37.3, 37.0, 36.85, 36.95, 37.1],
        borderColor: "#333",
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 20,
        max: 50,
        grid: {
          color: "#748073",
        },
      },
      x: {
        grid: {
          color: "#748073",
        },
      },
    },
  },
};
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);
export default {
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Line,
  },
  data: () => ({
    ...chartConfig,
    thumbnails: [
      "https://via.placeholder.com/100x100.png?text=10:00",
      "https://via.placeholder.com/100x100.png?text=10:15",
      "https://via.placeholder.com/100x100.png?text=10:30",
      "https://via.placeholder.com/100x100.png?text=10:45",
      "https://via.placeholder.com/100x100.png?text=11:00",
    ],
  }),
};
</script>
<template>
  <section class="section">
    <div class="container">
      <RouterLink to="/">&lt;&lt; Home</RouterLink>
      <h1 class="title">Experiment Title</h1>
      <p class="subtitle">Experiment Started on: <b>01/01/2023 12:00 AM</b></p>
      <div class="columns">
        <div class="column">
          <Line :data="data" :options="options" />
        </div>
        <div class="column">
          <img
            src="https://via.placeholder.com/300x300.png"
            alt="Experiment Photo"
          />
        </div>
      </div>
    </div>
    <div class="columns is-multiline">
      <div class="column is-one-fifth" v-for="thumb in thumbnails" :key="thumb">
        <div class="card">
          <div class="card-image">
            <figure class="image is-4by3">
              <img :src="thumb" alt="Thumbnail Image" />
            </figure>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
