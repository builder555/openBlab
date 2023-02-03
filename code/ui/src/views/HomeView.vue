<script>
export default {
  data: () => ({
    snapshotRate: 1,
    temperature: 37,
    specimen: "",
    baseUrl: `${window.location.protocol}//${window.location.hostname}:8000/`,
    experiments: [],
  }),
  computed: {
    isRunning() {
      return this.experiments && this.experiments.some((e) => e.is_running);
    },
  },
  methods: {
    async fetchExperiments() {
      const resp = await fetch(`${this.baseUrl}experiments`);
      this.experiments = await resp.json();
      this.experiments = this.experiments.reverse();
    },
    async startExperiment() {
      await fetch(`${this.baseUrl}experiments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          snapshots_hr: this.snapshotRate,
          temperature: this.temperature,
          specimen: this.specimen,
        }),
      });
      await this.fetchExperiments();
    },
    async stopExperiment(experimentId) {
      await fetch(`${this.baseUrl}experiments/${experimentId}/stop`, {
        method: "PUT",
      });
      this.experiments = this.experiments.map((e) => {
        if (e.id === experimentId) {
          return { ...e, is_running: false };
        }
        return e;
      });
    },
    changeDark() {
      window.matchMedia("(prefer-color-scheme: light)");
    },
  },
  mounted() {
    this.fetchExperiments();
  },
};
</script>
<template>
  <section class="hero is-fullheight">
    <div class="hero-body">
      <div class="login">
        <div class="block header">
          <img
            src="petri-monitor-sm.png"
            alt="logo"
            width="80"
            align="left"
            style="margin-top: -24px"
          />
          <h1 class="title is-1 has-text-grey block">OpenBLab</h1>
        </div>
        <section class="container">
          <div class="columns is-multiline">
            <div class="column is-8 is-offset-2 register">
              <div class="columns">
                <div class="column left">
                  <img
                    src="https://via.placeholder.com/450x450?text=no camera"
                    alt=""
                  />
                </div>
                <div class="column right has-text-centered">
                  <form @submit.stop.prevent="startExperiment">
                    <div class="field">
                      <div class="control">
                        <input
                          v-model="specimen"
                          class="input is-medium is-rounded"
                          type="text"
                          placeholder="Specimen"
                          required
                        />
                      </div>
                    </div>
                    <div class="field">
                      Snapshot frequency
                      <div
                        class="has-border-radius-medium has-border-color-black"
                      >
                        <input
                          v-model="snapshotRate"
                          type="range"
                          min="1"
                          max="30"
                          class="slider-input"
                        />
                        {{ snapshotRate }}/hr
                      </div>
                    </div>
                    <div class="field">
                      Temperature
                      <div
                        class="has-border-radius-medium has-border-color-black"
                      >
                        <input
                          v-model="temperature"
                          type="range"
                          min="25"
                          max="50"
                          class="slider-input"
                        />
                        {{ temperature }}ºC
                      </div>
                    </div>
                    <button
                      class="button is-block is-fullwidth is-medium is-rounded is-primary"
                      type="submit"
                    >
                      Start
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </section>
        <br />
        <nav class="panel">
          <p class="panel-heading">Experiments</p>
          <a
            v-for="experiment in experiments"
            :key="experiment.id"
            class="panel-block"
          >
            <span class="panel-icon" @click="stopExperiment(experiment.id)">
              <i
                class="fa-circle"
                :class="{
                  fas: experiment.is_running,
                  far: !experiment.is_running,
                }"
              ></i>
            </span>
            {{ experiment.specimen }} - {{ experiment.temperature }}ºC
          </a>
        </nav>
      </div>
    </div>
  </section>
</template>
