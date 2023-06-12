import { Validator } from 'vee-validate'
import { format } from 'date-fns'

Validator.extend('isDate', {
  getMessage(field) {
    return `${field} should be a valid date, IE: 2017/01/15`
  },
  validate(value) {
    return !!(value instanceof Date && value.toJSON())
  },
})
export const fetchProjectData = async (store, params, error) => {
  try {
    await store.dispatch('projects/setCurrentProject', params.id)
    await Promise.all([
      store.dispatch('project/loadProject', params.id),
      store.dispatch('projects/loadProjectStructure'),
    ])
  } catch (e) {
    console.warn('loadProjectData failed', e)
    error({
      response: {
        status: 404,
        statusText: 'This project does not exist',
      },
    })
    return Promise.reject(e)
  }
}

export const epochCheck = (date, present = true) => {
  if (date) {
    const secondsSinceEpoch = Math.round(date.getTime() / 1000)
    if (secondsSinceEpoch === 0) {
      return present ? new Date() : ''
    }
  }
  return date
}

export const newStages = (draft) => {
  return draft
    .filter((i) => i.checked)
    .map((i) => {
      return {
        id: i.id,
        note: i.note || null,
        date: formatDate(i.date),
      }
    })
}

export const formatDate = (date) => (format(date, 'YYYY-MM-DD') === 'Invalid Date' ? null : format(date, 'YYYY-MM-DD'))

export const projectFields = () => ({
  name: null,
  organisation: null,
  country: null,
  region: null,
  country_office: null,
  created: null,
  modified: null,
  implementation_overview: null,
  research: false,
  start_date: null,
  end_date: null,
  end_date_note: null,
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
  unicef_leading_sector: [],
  unicef_supporting_sectors: [],
  functions: [],
  hardware: [],
  nontech: [],
  regional_priorities: [],
  wbs: [],
  innovation_categories: [],
  cpd: [],
  partners: [],
  links: [],
  overview: '',
  coverImage: [],
  program_targets: '',
  program_targets_achieved: '',
  current_achievements: '',
  awp: '',
  total_budget_narrative: '',
  funding_needs: '',
  partnership_needs: '',
  target_group_reached: null,
  currency: null,
  total_budget: null,
  innovation_ways: [],
  isc: null,
  phase: null,
  stages: [],
  stagesDraft: null,
  stagesPrepared: null,
})

export const draftRules = () => {
  return {
    target_group_reached: {},
    currency: {},
    total_budget: {},
    cbd: {},
    innovation_ways: {},
    isc: {},
    start_date: {
      isDate: true,
    },
    end_date: {
      isDate: true,
    },
    end_date_note: {},
    stages: {},
    partner_name: {
      required: true,
      max: 100,
    },
    partner_contact: {
      max: 100,
    },
    partner_email: {
      email: true,
      required: false,
      max: 100,
    },
    partner_website: {
      url: { require_protocol: true },
      max: 2048,
    },
    link_website: {
      url: { require_protocol: true },
      max: 2048,
    },
    wbs: {
      max: 30,
    },
    unicef_sector: {
      required: false,
    },
    unicef_leading_sector: {
      required: false,
    },
    unicef_supporting_sectors: {
      required: false,
    },
    regional_priorities: {
      required: false,
    },
    hardware: {
      required: false,
    },
    nontech: {
      required: false,
    },
    functions: {
      required: false,
    },
    name: {
      required: true,
      min: 1,
      max: 128,
    },
    country_office: {
      required: true,
    },
    organisation: {
      required: false,
      max: 128,
    },
    contact_name: {
      max: 256,
    },
    contact_email: {
      required: false,
    },
    team: {
      required: true,
      min: 1,
    },
    implementation_overview: {
      max: 1024,
    },
    overview: {
      max: 300,
    },
    program_targets: {
      max: 1024,
    },
    program_targets_achieved: {
      max: 1024,
    },
    current_achievements: {
      max: 2048,
    },
    awp: {
      max: 500,
    },
    total_budget_narrative: {
      max: 500,
    },
    funding_needs: {
      max: 500,
    },
    partnership_needs: {
      max: 500,
    },
  }
}
export const publishRules = () => {
  return {
    partner_contact: {
      max: 100,
    },
    partner_name: {
      required: true,
      max: 100,
    },
    partner_email: {
      email: true,
      required: false,
      max: 100,
    },
    partner_website: {
      url: { require_protocol: true },
      max: 2048,
    },
    link_website: {
      url: { require_protocol: true },
      max: 2048,
    },
    wbs: {
      max: 30,
    },
    unicef_sector: {
      required: true,
    },
    unicef_leading_sector: {
      required: true,
    },
    unicef_supporting_sectors: {
      required: false,
    },
    regional_priorities: {
      required: false,
    },
    hardware: {
      required: false,
    },
    nontech: {
      required: false,
    },
    functions: {
      required: false,
    },
    name: {
      required: true,
      min: 1,
      max: 128,
    },
    overview: {
      required: true,
      min: 1,
      max: 300,
    },
    organisation: {
      required: true,
      max: 128,
    },
    country_office: {
      required: true,
    },
    geographic_scope: {
      max: 1024,
    },
    start_date: {
      required: true,
      isDate: true,
    },
    end_date: {
      required: false,
      isDate: true,
    },
    end_date_note: {
      required: false,
    },
    stages: {
      data: {
        required: true,
      },
    },
    contact_name: {
      required: true,
      max: 256,
    },
    contact_email: {
      required: true,
    },
    team: {
      required: true,
    },
    goal_area: {
      required: true,
    },
    capability_levels: {},
    capability_categories: {},
    capability_subcategories: {},
    platforms: {
      required: true,
    },
    strategies: {
      required: true,
      min: 1,
    },
    health_focus_areas: {
      required: true,
      min: 1,
    },
    hsc_challenges: {
      required: true,
      min: 1,
    },
    donors: {
      required: false,
    },
    implementation_dates: {},
    licenses: {},
  }
}
