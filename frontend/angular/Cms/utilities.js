import { format } from 'date-fns';

const prettifyDate = ({ created }) => {
  // 3:26 pm — 4 May, 2015
  return format(created, 'D MMM, YYYY');
};

const itemType = (item) => {
  if (item) {
    const typeLib = ['Resources', 'Tips & Considerations', 'Experiences'];
    return typeLib[item.type - 1];
  }
  return '';
};

const levenshtein = (a, b) => {
  if (a.length === 0) {
    return b.length;
  }
  if (b.length === 0) {
    return a.length;
  }
  let tmp;
  let i;
  let j;
  let prev;
  let val;
  if (a.length > b.length) {
    tmp = a;
    a = b;
    b = tmp;
  }

  const row = Array(a.length + 1);
  for (i = 0; i <= a.length; i++) {
    row[i] = i;
  }

  for (i = 1; i <= b.length; i++) {
    prev = i;
    for (j = 1; j <= a.length; j++) {
      if (b[i - 1] === a[j - 1]) {
        val = row[j - 1];
      } else {
        val = Math.min(row[j - 1] + 1,
          Math.min(prev + 1,
            row[j] + 1));
      }
      row[j - 1] = prev;
      prev = val;
    }
    row[a.length] = prev;
  }
  return row[a.length];
};

const normalizeName = (name) => {
  return name.toLowerCase().replace('&', 'and').replace(/ /g, '-');
};

const postProcessHtml = (html) => {
  return html.replace(/<a(.+?<\/a>)/g, (match, groupOne) => {
    return `<a target="_blank"${groupOne.trim()}`;
  });
};

export {
  prettifyDate,
  itemType,
  levenshtein,
  normalizeName,
  postProcessHtml
};
