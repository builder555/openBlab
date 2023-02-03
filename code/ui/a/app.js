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
      // console.log(JSON.parse(JSON.stringify(this.experiments)));
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
  },
  mounted() {
    this.fetchExperiments();
  },
};
