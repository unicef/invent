export const state = () => ({
  queue: []
});
export const getters = {
  getQueue: state => state.queue
};
export const actions = {
  async loadQueue ({ commit, state }) {
    if (!state.queue || state.queue.length === 0) {
      const { data } = await this.$axios.get('/api/projects/import/');
      console.log(data)
      commit('SET_QUEUE', data);
    }
  },
  async addDataToQueue ({ commit, state }, imported) {
    const { data } = await this.$axios.post(`api/projects/import/`, imported);
    const newQueue = [
      ...state.queue,
      data
    ];
    commit('SET_QUEUE', newQueue);
    return data;
  }
};

export const mutations = {
  SET_QUEUE: (state, queue) => {
    state.queue = queue;
  }
};
