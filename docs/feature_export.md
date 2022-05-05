## Export initiatives

There are two ways to export initiative.

### From Django admin


### From application

#### ListExport component

The `ListExport` is a renderless component that after parsing the selected initiatives (projects), passes back the parsed data to the parent component via the default scope slot.

The export is handled by the [JS to XLXS components group](https://vue-xlsx.netlify.app/components/js-to-xlsx.html) that is part of the [vue-xlsx](https://vue-xlsx.netlify.app/) package.

##### The export workflow
- user selects a project
- the `ListExport` component runs the parsing immediatelly which triggers
- `xlsx-workbook` and `xlsx-sheet` to be "rendered", ready to be downloaded
- download link pressed, the `xlsx-download` initiates the download

##### Parsing projects

The raw project list from the backend doesn't contain all the data that is displayed throughout the application, it needs to be prepared or converted on the frontend for the actual purpose. We call this preparation *parsing*.
In order to parse the projects, a field map (`colKeyValues`) needed to be defined with properties and a parse function. There are some general fields, but there are some special ones, like `health_focus_areas`.

```js
{
  id: '10',
  label: 'Health Focus Areas',
  key: 'health_focus_areas',
  parse: (health_focus_areas) =>
    this.parseHealthFocusAreas(health_focus_areas),
}
```

#### Inventory

The inventory list export used the simple `parsed` scoped slot, but further features have been added to the ListExport components, so now it's obsolete, the `parsedScores` scoped slot is used throughout the application.

#### Portfolio

In the portfolio manager the initiatives can be in three different state:
1. Inventory  
   As the name implies, it's the same as the Inventory list.
2. For review  
   This list displays the review scores (Scoring) and Questionnaires Assigned if there is any. These are complex data structures, that needs special handling when parsing the project list. The vertical data is parsed into horizontal data.
3. Portfolio  
   From export point of view, it is the same as the `For review` list, it contains