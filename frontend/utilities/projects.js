export const fetchProjectData = async (store, params, error) => {
  try {
    await store.dispatch('projects/setCurrentProject', params.id);
    await Promise.all([
      store.dispatch('project/loadProject', params.id),
      store.dispatch('projects/loadProjectStructure')
    ]);
  } catch (e) {
    console.warn('loadProjectData failed', e);
    error({
      response: {
        status: 404,
        statusText: 'This project does not exist'
      }
    });
    return Promise.reject(e);
  }
};

export const projectFields = () => ({
  name: null,
  organisation: 56,
  country: null,
  country_office: null,
  modified: null,
  field_office: null,
  implementation_overview: null,
  start_date: null,
  end_date: null,
  contact_name: null,
  contact_email: null,
  team: [],
  viewers: [],
  goal_area: null,
  result_area: null,
  capability_levels: [],
  capability_categories: [],
  capability_subcategories: [],
  platforms: [],
  dhis: [],
  health_focus_areas: [],
  hsc_challenges: [],
  donors: []
});

export const draftRules = () => {
  return {
    name: {
      required: true,
      min: 1,
      max: 128
    },
    country_office: {
      required: true
    },
    organisation: {
      required: false,
      max: 128
    },
    contact_name: {
      max: 256
    },
    contact_email: {
      email: true
    },
    team: {
      required: true,
      min: 1
    },
    implementation_overview: {
      max: 1024
    }
  };
};
export const publishRules = () => {
  return {
    name: {
      required: true,
      min: 1,
      max: 128
    },
    organisation: {
      required: true,
      max: 128
    },
    country_office: {
      required: true
    },
    geographic_scope: {
      max: 1024
    },
    start_date: {
      required: true
    },
    end_date: {
      required: false
    },
    contact_name: {
      required: true,
      max: 256
    },
    contact_email: {
      email: true,
      required: true
    },
    team: {
      required: true
    },
    goal_area: {
      required: true
    },
    capability_levels: {
    },
    capability_categories: {
    },
    capability_subcategories: {
    },
    platforms: {
      required: true
    },
    strategies: {
      required: true,
      min: 1
    },
    health_focus_areas: {
      required: true,
      min: 1
    },
    hsc_challenges: {
      required: true,
      min: 1
    },
    donors: {
      required: false
    },
    implementation_dates: {},
    licenses: {}
  };
};
