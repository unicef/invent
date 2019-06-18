/* eslint prefer-promise-reject-errors: 0 */
import * as api from '~/utilities/api';

const emptyTest = (fn, expected) => {
  const result = fn();
  expect(result).toEqual(expected);
};

const wrongInputTest = (fn, expected, objectIsValid = false) => {
  jest.spyOn(console, 'warn').mockReturnValue(null);
  let result = fn(1);
  expect(result).toEqual(expected);
  result = fn('a');
  expect(result).toEqual(expected);

  result = fn({});
  expect(result).toEqual(expected);

  expect(console.warn).toHaveBeenCalledTimes(objectIsValid ? 2 : 3);
};

describe('coverageMapper', () => {
  test('returns one array with an array and an object inside', () => {
    const result = api.coverageMapper([]);
    expect(result).toEqual([[], {}]);
  });

  test('does not fail with empty input', () => {
    emptyTest(api.coverageMapper, [[], {}]);
  });

  test('does not fail with wrong input', () => {
    wrongInputTest(api.coverageMapper, [[], {}]);
  });

  test('convert an array of object', () => {
    const original = [
      {
        district: 'd',
        clients: 1,
        facilities: 2,
        health_workers: 3
      }
    ];
    const result = api.coverageMapper(original);
    expect(result[0]).toEqual(['d']);
    expect(result[1]).toEqual({
      'd': {
        clients: 1,
        facilities: 2,
        health_workers: 3,
        facilities_list: undefined
      }
    });
  });

  test('if facilities_list is present override facilities', () => {
    const original = [
      {
        district: 'd',
        clients: 1,
        facilities: 2,
        health_workers: 3,
        facilities_list: [1, 2, 3, 4]
      }
    ];
    const result = api.coverageMapper(original);
    expect(result[0]).toEqual(['d']);
    expect(result[1]).toEqual({
      'd': {
        clients: 1,
        facilities: 4,
        health_workers: 3,
        facilities_list: [1, 2, 3, 4]
      }
    });
  });
});

describe('interoperabilityLinksMapper', () => {
  test('return an object', () => {
    const result = api.interoperabilityLinksMapper([]);
    expect(result).toEqual({});
  });

  test('does not fail with empty input', () => {
    emptyTest(api.interoperabilityLinksMapper, {});
  });

  test('does not fail with wrong input', () => {
    wrongInputTest(api.interoperabilityLinksMapper, {});
  });

  test('convert an array into an object', () => {
    const original = [
      { id: 1, link: 'a', selected: true }
    ];
    const result = api.interoperabilityLinksMapper(original);
    expect(result).toEqual({ 1: { link: 'a', selected: true } });
  });
});

describe('platformsMapper', () => {
  test('return an array with two arrays inside', () => {
    const result = api.platformsMapper([]);
    expect(result).toEqual([[], []]);
  });

  test('does not fail with empty input', () => {
    emptyTest(api.platformsMapper, [[], []]);
  });

  test('does not fail with wrong input', () => {
    wrongInputTest(api.platformsMapper, [[], []]);
  });

  test('convert an array of objects', () => {
    const original = [
      { id: 1, strategies: [1] }
    ];
    const result = api.platformsMapper(original);
    expect(result[0]).toEqual([1]);
    expect(result[1]).toEqual([{ id: 1, platform: 1 }]);
  });

  test('does not fail for missing or malformed inner data', () => {
    const original = [
      { id: 1 }
    ];
    let result = api.platformsMapper(original);
    expect(result).toEqual([[1], []]);

    original[0].strategies = 1;
    result = api.platformsMapper(original);
    expect(result).toEqual([[1], []]);

    original[0].strategies = '';
    result = api.platformsMapper(original);
    expect(result).toEqual([[1], []]);
  });
});

describe('countryCustomFieldMapper', () => {
  test('returns an array', () => {
    const result = api.countryCustomFieldMapper({});
    expect(result).toEqual([]);
  });

  test('does not fail with empty input', () => {
    emptyTest(api.countryCustomFieldMapper, []);
  });

  test('does not fail with wrong input', () => {
    wrongInputTest(api.countryCustomFieldMapper, [], true);
  });

  test('convert an object in an array of objects', () => {
    const original = {
      1: ['yes']
    };
    const result = api.countryCustomFieldMapper(original);
    expect(result).toEqual([{ question_id: 1, answer: ['yes'] }]);
  });
});

describe('countryCustomFieldMapper', () => {
  test('returns an array', () => {
    const result = api.countryCustomFieldMapper({});
    expect(result).toEqual([]);
  });

  test('does not fail with empty input', () => {
    emptyTest(api.countryCustomFieldMapper, []);
  });

  test('does not fail with wrong input', () => {
    wrongInputTest(api.countryCustomFieldMapper, [], true);
  });

  test('convert an object in an array of objects', () => {
    const original = {
      1: ['yes']
    };
    const result = api.countryCustomFieldMapper(original);
    expect(result).toEqual([{ question_id: 1, answer: ['yes'] }]);
  });
});

describe('donorCustomFieldMapper', () => {
  test('returns an array', () => {
    const result = api.donorCustomFieldMapper({});
    expect(result).toEqual([]);
  });

  test('does not fail with empty input', () => {
    emptyTest(api.donorCustomFieldMapper, []);
  });

  test('does not fail with wrong input', () => {
    wrongInputTest(api.donorCustomFieldMapper, [], true);

    const wrongInside = {
      1: 1
    };
    const result = api.donorCustomFieldMapper(wrongInside);
    expect(result).toEqual([]);
    expect(console.warn).toHaveBeenCalledTimes(3);
  });

  test('convert an object in an array of objects', () => {
    const original = {
      1: {
        11: ['yes']
      }
    };
    const result = api.donorCustomFieldMapper(original);
    expect(result).toEqual([{ question_id: 11, answer: ['yes'], donor_id: 1 }]);
  });
});

describe('apiReadParser', () => {
  test('returns an object', () => {
    const result = api.apiReadParser({});
    expect(result).toEqual(expect.any(Object));
  });

  test('calls all the api parsing functions', () => {
    jest.spyOn(api.lib, 'coverageMapper').mockReturnValue([1, 2]);
    jest.spyOn(api.lib, 'platformsMapper').mockReturnValue([1, 2]);
    jest.spyOn(api.lib, 'interoperabilityLinksMapper').mockReturnValue(1);
    jest.spyOn(api.lib, 'parseCustomAnswers').mockReturnValue({});
    jest.spyOn(api.lib, 'countryCustomFieldMapper').mockReturnValue([]);
    jest.spyOn(api.lib, 'donorCustomFieldMapper').mockReturnValue([]);

    api.apiReadParser({});

    expect(api.lib.coverageMapper).toHaveBeenCalled();
    expect(api.lib.platformsMapper).toHaveBeenCalled();
    expect(api.lib.interoperabilityLinksMapper).toHaveBeenCalled();
    expect(api.lib.parseCustomAnswers).toHaveBeenCalled();
    expect(api.lib.countryCustomFieldMapper).toHaveBeenCalled();
    expect(api.lib.donorCustomFieldMapper).toHaveBeenCalled();
  });

  test('coverageType is set accordingly', () => {
    const coverageMapper = jest.spyOn(api.lib, 'coverageMapper').mockReturnValue([1, 2]);
    let result = api.apiReadParser({});
    expect(result.coverageType).toEqual(1);
    coverageMapper.mockReturnValue([undefined, null]);
    result = api.apiReadParser({});
    expect(result.coverageType).toEqual(2);
  });
});

describe('isNullUndefinedOrEmptyString', () => {
  test('returns true for null undefined and empty string', () => {
    expect(api.isNullUndefinedOrEmptyString(null)).toEqual(true);
    expect(api.isNullUndefinedOrEmptyString(undefined)).toEqual(true);
    expect(api.isNullUndefinedOrEmptyString('')).toEqual(true);
    expect(api.isNullUndefinedOrEmptyString(1)).toEqual(false);
  });
});

describe('isEmpty', () => {
  test('return false if is an Array', () => {
    expect(api.isEmpty([])).toEqual(false);
  });
  test('return false if is a Date', () => {
    expect(api.isEmpty(new Date())).toEqual(false);
  });
  test('if is an Object returns true if the object has no keys', () => {
    expect(api.isEmpty({})).toEqual(true);
    expect(api.isEmpty({ foo: 'bar' })).toEqual(false);
  });
  test('in any other case it invoke isNullUndefinedOrEmptyString', () => {
    jest.spyOn(api.lib, 'isNullUndefinedOrEmptyString').mockReturnValue(undefined);
    api.isEmpty(null);
    api.isEmpty('');
    api.isEmpty(1);
    api.isEmpty('foo');
    expect(api.lib.isNullUndefinedOrEmptyString).toHaveBeenCalledTimes(4);
  });
});
