import fs from 'fs';
beforeEach(() => {
  // Delete all files in the download directory
  fs.readdirSync('./cypress/e2e/downloads/').forEach((file) => {
    fs.unlinkSync(`./cypress/e2e/downloads/${file}`);
  });
});