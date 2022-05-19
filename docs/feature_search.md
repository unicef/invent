# Search

The search functionality is a filtering system that uses different input fields. So every field has an attached model value to it. The model value is loaded from the store.

So if there is a dropdown of `regions` we have a `mapGetter`

```js
...mapGetters({
    regions: 'system/getRegions'
    // more code
```

We also map the state of the filter from store state into a local variable. This means we load what was the chosen `region`

```js
...mapState({
    region: (state) => state.search.filter.region,
    // more code
```
So now we have a list as `this.regions` and the current selection `this.region`. The default to every filter query is set in the `frontend/store/search.js` on the definition of state:

```js
export const state = () => ({
  ...stateGenerator(),
  blockSearch: true,
  filter: {
    // ** SEARCH PARAMETERS **
    q: '',
    in: ['name', 'overview', 'desc', 'ach', 'partner', 'id'],
    // ** FILTER PARAMETERS **
    country: [], // `country` eg: country=1&country=2
    sw: [], // `sw` eg: sw=1&sw=2
    dhi: [], // `dhi` eg: dhi=1&dhi=2
    hfa: [], // `hfa` eg: hfa=1&hfa=2
    hsc: [], // `hsc` eg: hsc=1&hsc=2
    // `his` eg: his=1&his=2
    region: '',
    // more code
```

Then these loaded data fetched to the actual filter input:

:::
<filter-select
    :value="region"
    :items="regions"
    :placeholder="$gettext('Region') | translate"
    @change="handleSearch('region', $event, regions)"
/>
:::

On the `@change` event we set a `handleSearch` search call which will update the filter in the store and reload the API endpoint for the search.

Some filters set to trigger the change inside a `watch`:

```js
watch: {
    selectedDHI() {
        this.handleSearch('dhi', this.selectedDHI)
    },
    // more code
```

## Frontend

There's two almost identical component for search, called `AdvSearch`. These are differences between them:

### @components/dashboard/AdvSearch

Used in **Inventory**

This component has a url query interpreter for the filter. So if you copy the link of the current filter set, you can share a filtered view of the projects with someone else. So this file has the following additionally to handle the query in the link:
- `...mapState` spread for all the shortened link query parameters
- `handleSearch()` function which calls `setSearch()` which uses the store and sets the respective query parameters. Then in the `handleSearch()` we invoke the `getSearchResult()` which calls the `getSearch()` and that is actually reloading the list of projects.

### @components/search/AdvSearch

Used in **Portfolio manager**

This component do not have a `handleSearch()`, and does all the loading of options and loading the defaults using the `...mapGettersActions`:
```js
...mapGettersActions({
    selectedGoal: ['dashboard', 'getSelectedGoal', 'setSelectedGoal', 0],
    selectedResult: [
        'dashboard',
        'getSelectedResult',
        'setSelectedResult',
        0,
    ],
    selectedDHI: ['dashboard', 'getSelectedDHI', 'setSelectedDHI', 0],
    selectedHFA: ['dashboard', 'getSelectedHFA', 'setSelectedHFA', 0],
    selectedHSC: ['dashboard', 'getSelectedHSC', 'setSelectedHSC', 0],
```
These contain the getters and setters for a given filter.
The store functions will handle the portfolio filtering in the portfolio, dashboard and search stores.
