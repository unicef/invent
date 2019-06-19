import get from 'lodash/get';
export const coverageMapper = collection => {
  const coverage = [];
  const coverageData = {};
  collection = collection || [];
  if (Array.isArray(collection)) {
    collection.forEach(c => {
      coverage.push(c.district);
      coverageData[c.district] = {
        clients: c.clients,
        facilities: c.facilities_list ? c.facilities_list.length : c.facilities,
        health_workers: c.health_workers,
        facilities_list: c.facilities_list
      };
    });
  } else {
    console.warn('Invalid or malformed input passed to api/coverageMapper');
  }
  return [coverage, coverageData];
};

export const interoperabilityLinksMapper = links => {
  const result = {};
  links = links || [];
  if (Array.isArray(links)) {
    links.forEach(l => {
      result[l.id] = {
        link: l.link,
        selected: l.selected
      };
    });
  } else {
    console.warn('Invalid or malformed input passed to api/interoperabilityLinksMapper');
  }
  return result;
};

export const platformsMapper = collection => {
  const platforms = [];
  const digitalHealthInterventions = [];
  collection = collection || [];
  if (Array.isArray(collection)) {
    collection.forEach(p => {
      platforms.push(p.id);
      if (p.strategies && Array.isArray(p.strategies)) {
        digitalHealthInterventions.push(...p.strategies.map(s => ({ id: s, platform: p.id })));
      }
    });
  } else {
    console.warn('Invalid or malformed input passed to api/platformsMapper');
  }
  return [platforms, digitalHealthInterventions];
};

export const countryCustomFieldMapper = collection => {
  const customAnswers = [];
  if (typeof collection === 'object' && collection) {
    for (let key in collection) {
      customAnswers.push({ question_id: +key, answer: collection[key] });
    }
  } else {
    console.warn('Invalid or malformed input passed to api/countryCustomFieldMapper');
  }
  return customAnswers;
};

export const donorCustomFieldMapper = collection => {
  const customAnswers = [];
  if (typeof collection === 'object' && !Array.isArray(collection) && collection) {
    for (let donor in collection) {
      if (typeof collection[donor] === 'object' && !Array.isArray(collection) && collection) {
        for (let key in collection[donor]) {
          customAnswers.push({ question_id: +key, answer: collection[donor][key], donor_id: +donor });
        }
      } else {
        console.warn('Malformed input passed to api/countryCustomFieldMapper');
      }
    }
  } else {
    console.warn('Invalid or malformed input passed to api/countryCustomFieldMapper');
  }
  return customAnswers;
};

export const apiReadParser = p => {
  const [ platforms, digitalHealthInterventions ] = lib.platformsMapper(p.platforms);
  p = lib.parseCustomAnswers(p);
  const donor_custom_answers = lib.donorCustomFieldMapper(p.donor_answers);
  return { ...p,
    platforms,
    digitalHealthInterventions,
    donor_custom_answers
  };
};

export const isNullUndefinedOrEmptyString = value => value === null || value === undefined || value === '';

export const isEmpty = (value) => {
  if (Array.isArray(value)) {
    return false;
  } else if (value instanceof Date) {
    return false;
  } else if (value instanceof Object && value !== null) {
    return Object.keys(value).length === 0;
  }
  return lib.isNullUndefinedOrEmptyString(value);
};

export const dataCleaner = value => {
  if (Array.isArray(value)) {
    const result = value.filter(v => !lib.isNullUndefinedOrEmptyString(v));
    return result;
  }
  return value;
};

export const interoperabilityLinkWriteParser = links => {
  const result = [];
  for (let link in links) {
    const value = { ...links[link] };
    value.selected = value.selected ? true : undefined;
    value.link = !value.selected || lib.isNullUndefinedOrEmptyString(value.link) ? undefined : value.link;
    const item = { id: link, ...value };
    result.push(item);
  }
  return result.sort((a, b) => a.index - b.index).map(r => ({ ...r, index: undefined }));
};

export const platformsWriteParser = (platforms, digitalHealthInterventions) => {
  return platforms.map(p => {
    const strategies = [...digitalHealthInterventions.filter(dhi => dhi.platform === p).map(f => f.id)];
    return { id: p, strategies: strategies || [] };
  });
};

export const coverageWriteParser = (coverage, coverageData) => {
  return coverage.map(district => {
    const data = coverageData[district];
    return {
      district,
      ...data,
      clients: get(data, 'clients', 0),
      health_workers: get(data, 'health_workers', 0),
      facilities: get(data, 'facilities', 0)
    };
  });
};

export const customCountryAnswerParser = (customAnswers = []) => {
  return customAnswers.map(c => ({
    ...c,
    answer: c.answer[0] ? c.answer : []
  }));
};

export const customDonorAnswerParser = (customAnswers = [], donors = []) => {
  const result = donors.reduce((a, c) => {
    a[c] = [];
    return a;
  }, {});
  customAnswers.forEach(a => {
    const donor = a.donor_id;
    if (!result[donor]) {
      result[donor] = [];
    }
    result[donor].push({
      ...a,
      answer: a.answer[0] ? a.answer : [],
      donor_id: undefined });
  });
  return result;
};

export const apiWriteParser = (p, countryCustomAnswers, donorsCustomAnswers) => {
  const result = {};
  for (let key in p) {
    const value = dataCleaner(p[key]);
    result[key] = isEmpty(value) ? undefined : value;
  }
  const platforms = platformsWriteParser(p.platforms, p.digitalHealthInterventions);

  const donor_custom_answers = customDonorAnswerParser(donorsCustomAnswers, p.donors);
  return {
    project: {
      ...result,
      platforms,
      digitalHealthInterventions: undefined,
      country_answers: undefined,
      donors_answers: undefined,
      modified: undefined
    },
    donor_custom_answers
  };
};

export const intArrayFromQs = item => {
  return item ? Array.isArray(item) ? item.map(i => +i) : [+item] : [];
};

export const strArrayFromQs = item => {
  return item ? Array.isArray(item) ? item : [item] : [];
};

export const queryStringComparisonParser = collection => {
  const result = {};
  for (let key in collection) {
    const item = collection[key];
    if (item === null) {
      result[key] = null;
    } else if (item && !Array.isArray(item)) {
      result[key] = '' + item;
    } else if (item && Array.isArray(item) && item.length > 0) {
      result[key] = item;
    }
  }
  return result;
};

export const questionWriteParser = (question, type, parent) => {
  return {
    is_active: question.is_active,
    type: +question.type,
    question: question.question,
    options: question.type > 3 ? question.options : [],
    private: question.is_private,
    required: question.required,
    [type]: parent.id
  };
};

export const customColumnsMapper = (columns, prefix) => {
  return columns.map(c => ({
    originalId: c.id,
    id: `${prefix}_${c.id}`,
    label: c.question,
    type: c.type,
    donorId: c.donor
  }));
};

export const parseCustomAnswers = r => {
  const donor_answers = {};
  if (r.donors) {
    r.donors.forEach(d => {
      donor_answers[d] = {
        ...(r.donor_custom_answers ? r.donor_custom_answers[d] : null),
        ...(r.donor_custom_answers_private ? r.donor_custom_answers_private[d] : null)
      };
    });
  }
  return {
    ...r,
    country_answers: {
      ...r.country_custom_answers,
      ...r.country_custom_answers_private
    },
    donor_answers,
    country_custom_answers: undefined,
    country_custom_answers_private: undefined,
    donor_custom_answers: undefined,
    donor_custom_answers_private: undefined
  };
};

export const APIError = (field, message) => {
  const error = new Error('APIError');
  error.response = {
    data: {
      project: {
        [field]: [message]
      }
    }
  };
  return error;
};

export const lib = {
  coverageMapper,
  platformsMapper,
  interoperabilityLinksMapper,
  parseCustomAnswers,
  countryCustomFieldMapper,
  donorCustomFieldMapper,
  isNullUndefinedOrEmptyString
};
