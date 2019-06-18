module.exports = {
  verbose: true,
  bail: true,
  collectCoverage: true,
  restoreMocks: true,
  collectCoverageFrom: [
    '**/store/**/*.js',
    '**/utilities/**/*.js'
  ],
  coverageDirectory: 'coverage',
  coverageThreshold: {
    './utilities/api.js/': {
      branches: 25,
      functions: 25,
      lines: 25,
      statements: 25
    }
  },
  moduleFileExtensions: [
    'js',
    'json',
    'vue'
  ],
  moduleNameMapper: {
    '~(.*)$': '<rootDir>/$1'
  },
  transform: {
    '^.+\\.js$': '<rootDir>/node_modules/babel-jest',
    '.*\\.(vue)$': '<rootDir>/node_modules/vue-jest'
  },
  testPathIgnorePatterns: [
    '/node_modules/',
    '/cypress/'
  ],
  setupFiles: ['<rootDir>/node_modules/regenerator-runtime/runtime'],
  snapshotSerializers: [
    '<rootDir>/node_modules/jest-serializer-vue'
  ]
};
