#!/usr/bin/env node
/**
 * Script to add missing date fields and last_modified to old blog posts
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const blogDir = path.join(__dirname, '..', 'blog');
const cutoffDate = new Date('2023-01-01');
const today = new Date().toISOString().split('T')[0];

let dateFixed = 0;
let lastModifiedAdded = 0;

function processPost(postPath) {
  const content = fs.readFileSync(postPath, 'utf-8');
  const { data, content: mdContent } = matter(content);
  
  let updated = false;
  
  // Extract date from folder name
  const folderName = path.basename(path.dirname(postPath));
  const dateMatch = folderName.match(/^(\d{4}-\d{2}-\d{2})-/);
  
  // Add missing date field
  if (dateMatch && !data.date) {
    data.date = dateMatch[1];
    updated = true;
    dateFixed++;
    console.log(`✓ Added date ${dateMatch[1]} to: ${folderName}`);
  }
  
  // Add last_modified to posts older than 2023
  if (data.date && !data.last_modified) {
    const postDate = new Date(data.date);
    if (postDate < cutoffDate) {
      data.last_modified = today;
      data.last_modified_note = 'Nội dung có thể đã lỗi thời. Vui lòng kiểm tra thông tin trước khi sử dụng.';
      updated = true;
      lastModifiedAdded++;
      console.log(`✓ Added last_modified to: ${folderName}`);
    }
  }
  
  if (updated) {
    const newContent = matter.stringify(mdContent, data);
    fs.writeFileSync(postPath, newContent);
  }
}

function walkDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      const indexFile = path.join(fullPath, 'index.md');
      if (fs.existsSync(indexFile)) {
        processPost(indexFile);
      }
      walkDir(fullPath);
    }
  }
}

console.log('Starting blog maintenance script...\n');
walkDir(blogDir);

console.log(`\n✅ Summary:`);
console.log(`   - Added date field to ${dateFixed} posts`);
console.log(`   - Added last_modified to ${lastModifiedAdded} outdated posts (pre-2023)`);
console.log(`\n📅 Today: ${today}`);
console.log(`📅 Cutoff for last_modified: ${cutoffDate.toISOString().split('T')[0]}`);