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
      email: true,
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
      email: true,
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
