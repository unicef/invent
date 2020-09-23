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
  donors: [],
  // INVENT
  unicef_sector: [],
  functions: [],
  hardware: [],
  nontech: [],
  regional_priorities: [],
  overview: '',
  program_targets: '',
  program_targets_achieved: '',
  current_achievements: '',
  awp: '',
  total_budget_narrative: '',
  funding_needs: '',
  partnership_needs: '',
  target_group_reached: 0,
  currency: 1,
  total_budget: 0,
  wbs: [],
  innovation_categories: [],
  cpd: [],
  phase: null
});

export const draftRules = () => {
  return {
    target_group_reached: {},
    currency: {},
    total_budget: {},
    phase: {},
    wbs: {
      max: 30
    },
    unicef_sector: {
      required: false
    },
    regional_priorities: {
      required: false
    },
    hardware: {
      required: false
    },
    nontech: {
      required: false
    },
    functions: {
      required: false
    },
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
    },
    overview: {
      max: 300
    },
    program_targets: {
      max: 1024
    },
    program_targets_achieved: {
      max: 1024
    },
    current_achievements: {
      max: 2048
    },
    awp: {
      max: 500
    },
    total_budget_narrative: {
      max: 500
    },
    funding_needs: {
      max: 500
    },
    partnership_needs: {
      max: 500
    }
  };
};
export const publishRules = () => {
  return {
    unicef_sector: {
      required: true
    },
    regional_priorities: {
      required: false
    },
    hardware: {
      required: false
    },
    nontech: {
      required: false
    },
    functions: {
      required: false
    },
    name: {
      required: true,
      min: 1,
      max: 128
    },
    overview: {
      required: true,
      min: 1,
      max: 300
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
