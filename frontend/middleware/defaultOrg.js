export default async function ({ app, redirect }) {
  const path = app.localePath({ name: 'organisation', params: { organisation: '-' } });
  redirect(path);
};
